"""Logical states, stabilizers, and circuit-level syndrome recovery for the
[[3,1,1]] bit-flip and phase-flip repetition codes.

The encoder is analytical (logical kets are constructed directly in numpy),
but syndrome extraction and correction are run as an honest qiskit circuit on
``AerSimulator(method='density_matrix')`` with ancilla qubits and classical
feed-forward conditionals. Numpy system-qubit ordering (qubit 0 leftmost in
the kron product) is preserved by reversing the qubit list when interfacing
qiskit, mirroring the convention used in :mod:`biqmn.core.simulator`.
"""
from __future__ import annotations

from typing import Sequence, Tuple

import numpy as np

from .hamiltonian import PAULI_I, PAULI_X, PAULI_Z


SUPPORTED_CODES: Tuple[str, ...] = ("bitflip", "phaseflip")

_BASIS_0 = np.array([1.0, 0.0], dtype=complex)
_BASIS_1 = np.array([0.0, 1.0], dtype=complex)
_BASIS_PLUS = np.array([1.0, 1.0], dtype=complex) / np.sqrt(2.0)
_BASIS_MINUS = np.array([1.0, -1.0], dtype=complex) / np.sqrt(2.0)


def _kron_triple(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    return np.kron(np.kron(a, b), c)


def _validated_code(code: str) -> str:
    key = str(code).strip().lower()
    if key not in SUPPORTED_CODES:
        raise ValueError(
            f"Unsupported QEC code {code!r}; expected one of {SUPPORTED_CODES}."
        )
    return key


def logical_basis(code: str) -> Tuple[np.ndarray, np.ndarray]:
    """Return ``(|0_L>, |1_L>)`` as 8-dim kets in numpy kron ordering."""
    key = _validated_code(code)
    if key == "bitflip":
        psi0 = _kron_triple(_BASIS_0, _BASIS_0, _BASIS_0)
        psi1 = _kron_triple(_BASIS_1, _BASIS_1, _BASIS_1)
    else:  # phaseflip
        psi0 = _kron_triple(_BASIS_PLUS, _BASIS_PLUS, _BASIS_PLUS)
        psi1 = _kron_triple(_BASIS_MINUS, _BASIS_MINUS, _BASIS_MINUS)
    return psi0, psi1


def logical_state(code: str, amplitudes: Sequence[complex]) -> np.ndarray:
    """Build ``c_0 |0_L> + c_1 |1_L>`` (normalised) as an 8-dim ket."""
    amps = list(amplitudes)
    if len(amps) != 2:
        raise ValueError("Repetition codes take exactly two logical amplitudes.")
    psi0, psi1 = logical_basis(code)
    state = complex(amps[0]) * psi0 + complex(amps[1]) * psi1
    norm = float(np.linalg.norm(state))
    if norm < 1.0e-14:
        raise ValueError("Logical amplitudes collapse to the zero vector.")
    return state / norm


def stabilizer_operators(code: str) -> list[np.ndarray]:
    """Return the two stabilizer generators as 8x8 operators."""
    key = _validated_code(code)
    if key == "bitflip":
        return [
            _kron_triple(PAULI_Z, PAULI_Z, PAULI_I),
            _kron_triple(PAULI_I, PAULI_Z, PAULI_Z),
        ]
    return [
        _kron_triple(PAULI_X, PAULI_X, PAULI_I),
        _kron_triple(PAULI_I, PAULI_X, PAULI_X),
    ]


def logical_operators(code: str) -> dict:
    """Return ``{'X_L': ..., 'Z_L': ..., 'stabilizers': [S1, S2]}`` as 8x8 matrices."""
    key = _validated_code(code)
    if key == "bitflip":
        X_L = _kron_triple(PAULI_X, PAULI_X, PAULI_X)
        Z_L = _kron_triple(PAULI_Z, PAULI_I, PAULI_I)
    else:
        X_L = _kron_triple(PAULI_Z, PAULI_Z, PAULI_Z)
        Z_L = _kron_triple(PAULI_X, PAULI_I, PAULI_I)
    return {"X_L": X_L, "Z_L": Z_L, "stabilizers": stabilizer_operators(key)}


def syndrome_probabilities(rho_data: np.ndarray, code: str) -> dict:
    """Return ``p(s_A, s_B)`` for the four syndrome outcomes and the no-error
    probability ``p(0,0)``. Stabilizers commute, so joint projectors factorise.
    """
    key = _validated_code(code)
    stabilizers = stabilizer_operators(key)
    S_A, S_B = stabilizers
    I8 = np.eye(8, dtype=complex)
    probs = {}
    for sa in (0, 1):
        sign_a = 1.0 if sa == 0 else -1.0
        P_A = 0.5 * (I8 + sign_a * S_A)
        for sb in (0, 1):
            sign_b = 1.0 if sb == 0 else -1.0
            P_B = 0.5 * (I8 + sign_b * S_B)
            P = P_A @ P_B
            probs[(sa, sb)] = float(np.real(np.trace(P @ rho_data @ P)))
    total = sum(probs.values())
    if total > 0:
        probs = {k: v / total for k, v in probs.items()}
    return {
        "probabilities": probs,
        "no_error_probability": float(probs.get((0, 0), 0.0)),
    }


def _apply_bitflip_syndrome(qc, data, anc, cr) -> None:
    # numpy qubit i maps to qiskit data[n_data - 1 - i] (see simulator.py)
    # syndrome A: parity of numpy q0, q1 = data[2], data[1]
    qc.cx(data[2], anc[0])
    qc.cx(data[1], anc[0])
    # syndrome B: parity of numpy q1, q2 = data[1], data[0]
    qc.cx(data[1], anc[1])
    qc.cx(data[0], anc[1])
    qc.measure(anc[0], cr[0])
    qc.measure(anc[1], cr[1])
    # classical integer value = cr[1] cr[0] (cr[0] is LSB)
    # (s_A=1, s_B=0) -> value 0b01=1 -> X on numpy q0 (data[2])
    with qc.if_test((cr, 1)):
        qc.x(data[2])
    # (s_A=1, s_B=1) -> value 0b11=3 -> X on numpy q1 (data[1])
    with qc.if_test((cr, 3)):
        qc.x(data[1])
    # (s_A=0, s_B=1) -> value 0b10=2 -> X on numpy q2 (data[0])
    with qc.if_test((cr, 2)):
        qc.x(data[0])


_ANC_ZERO_PROJECTOR = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)


def _embed_data_density(rho_data: np.ndarray) -> np.ndarray:
    """Return the 32x32 density on (anc[1], anc[0], data[2], data[1], data[0])
    whose data-register reduction is ``rho_data``, with ancillas in |00>.

    Because numpy qubit i ↔ qiskit data[2-i], the raw numpy 3-qubit density
    already matches qiskit kron ordering on the data register, so we just
    tensor |0><0| for each ancilla on the outside (MSB) of the kron product.
    """
    return np.kron(_ANC_ZERO_PROJECTOR, np.kron(_ANC_ZERO_PROJECTOR, rho_data))


def syndrome_recovery_kraus(code: str) -> tuple[np.ndarray, ...]:
    """Exact, full-information recovery operators C_s P_s in numpy ordering.

    Summing K_s rho K_s^dagger averages all ideal syndrome outcomes. This is
    not a decoder restricted to the subsequently corrupted controller symbols.
    """
    key = _validated_code(code)
    s1, s2 = stabilizer_operators(key)
    identity = np.eye(8, dtype=complex)
    error = PAULI_X if key == "bitflip" else PAULI_Z
    targets = {(0, 0): None, (1, 0): 0, (1, 1): 1, (0, 1): 2}
    operators = []
    for (a, b), target in targets.items():
        projector = ((identity + (-1)**a*s1)/2) @ ((identity + (-1)**b*s2)/2)
        factors = [error if i == target else PAULI_I for i in range(3)]
        operators.append(_kron_triple(*factors) @ projector)
    return tuple(operators)


def apply_syndrome_recovery(rho_data: np.ndarray, code: str, *,
                            method: str = "circuit", shots: int | None = None,
                            seed_simulator: int | None = None) -> np.ndarray:
    """Apply ideal full-syndrome recovery with explicit averaging semantics.

    Parameters
    ----------
    rho_data : (8, 8) complex ndarray
        3-qubit system density in numpy kron ordering (system qubit 0 leftmost).
    code : {"bitflip", "phaseflip"}
    method : {"circuit", "exact"}
        Legacy default ``circuit`` samples measurement outcomes in Aer.
        ``exact`` sums the four corrected syndrome branches deterministically.
    shots, seed_simulator : int, optional
        Circuit-only controls. Omitted values preserve the historical Aer
        defaults; reproducible finite-shot studies must set both explicitly.

    Returns
    -------
    (8, 8) complex ndarray
        Recovered 3-qubit density after running the syndrome circuit with
        ancillas + classical-feed-forward Pauli corrections, with ancillas
        traced out.
    """
    key = _validated_code(code)
    if method not in ("circuit", "exact"):
        raise ValueError("Recovery method must be 'circuit' or 'exact'.")
    rho = np.asarray(rho_data, dtype=complex)
    if rho.shape != (8, 8):
        raise ValueError(f"Expected an 8x8 density matrix, got shape {rho.shape}.")
    if not np.all(np.isfinite(rho)):
        raise ValueError("Recovery density matrix must be finite.")
    if method == "exact":
        if shots is not None or seed_simulator is not None:
            raise ValueError("Exact syndrome averaging does not use shots or a simulator seed.")
        # Do not renormalize or clip eigenvalues: this is a linear CPTP map.
        return sum(k @ rho @ k.conj().T for k in syndrome_recovery_kraus(key))
    for name, value, minimum in (("shots", shots, 1), ("seed_simulator", seed_simulator, 0)):
        if value is not None and (isinstance(value, (bool, np.bool_))
                or not isinstance(value, (int, np.integer)) or value < minimum):
            raise ValueError(f"{name} must be an integer >= {minimum}.")
    try:
        from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
        from qiskit_aer import AerSimulator
        from qiskit_aer.library import SetDensityMatrix
    except Exception as exc:  # pragma: no cover - import guard
        raise RuntimeError(
            "qiskit/qiskit-aer unavailable; cannot run circuit-level syndrome recovery."
        ) from exc

    data = QuantumRegister(3, "data")
    anc = QuantumRegister(2, "anc")
    cr = ClassicalRegister(2, "sy")
    qc = QuantumCircuit(data, anc, cr)

    qc.append(SetDensityMatrix(_embed_data_density(rho)), qc.qubits)

    if key == "phaseflip":
        for qubit in data:
            qc.h(qubit)
    _apply_bitflip_syndrome(qc, data, anc, cr)
    if key == "phaseflip":
        for qubit in data:
            qc.h(qubit)

    qc.save_density_matrix([data[0], data[1], data[2]], label="rho_data")

    backend = AerSimulator(method="density_matrix")
    run_options = {}
    if shots is not None:
        run_options["shots"] = int(shots)
    if seed_simulator is not None:
        run_options["seed_simulator"] = int(seed_simulator)
    result = backend.run(qc, **run_options).result()
    raw = result.data(0)["rho_data"]
    rho_out = np.asarray(raw.data if hasattr(raw, "data") else raw, dtype=complex)
    rho_out = 0.5 * (rho_out + rho_out.conj().T)
    trace = complex(np.trace(rho_out))
    if abs(trace) > 0.0:
        rho_out = rho_out / trace
    return rho_out
