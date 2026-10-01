"""R1: physically consistent finite-clock observability qualification.

This is multi-copy state estimation, not a QEC recovery channel or a C3R test.
The occupation spectrum is deliberately an invertible positive control, not a
claimed improvement over the raw data. See manuscript/revision_new_experiments_protocol.md.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone
import itertools
import json
from pathlib import Path
import sys
import time
import traceback

import numpy as np

from .common import REPO_ROOT
from .revision_audit import sha256, write_json

X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.diag([1., -1.]).astype(complex)
PAULIS = np.array([X, Y, Z])
OMEGA = .8
TAUS = np.arange(8)*np.pi/(8*OMEGA)
AXES = {"aligned": np.array([0., 0., 1.]), "tilted": np.array([1., 0., 1.])/np.sqrt(2)}
METHODS = ("raw_mixed_ls", "occupation_spectral_ls", "raw_pure_ls",
           "raw_nearest_reference", "legacy_spectral_nearest_reference")
PROTOCOL_PATH = REPO_ROOT.parent/"manuscript"/"revision_new_experiments_protocol.md"


def bloch_density(vector):
    return (np.eye(2) + np.einsum("i,ijk->jk", vector, PAULIS))/2


def pure_ket(vector):
    values, vectors = np.linalg.eigh(bloch_density(vector))
    return vectors[:, np.argmax(values)]


def logical_unitary(axis, tau):
    generator = np.einsum("i,ijk->jk", axis, PAULIS)
    return np.cos(OMEGA*tau)*np.eye(2) + 1j*np.sin(OMEGA*tau)*generator


def measurement_design(axis, taus=TAUS):
    rows = []
    for tau in taus:
        u = logical_unitary(axis, tau)
        observable = u.conj().T @ Z @ u
        rows.append([float(np.trace(observable @ p).real/2) for p in PAULIS])
    return np.array(rows)


def history_state(vector, code, axis):
    from ..core.encoding import logical_basis, logical_operators
    encoding = np.column_stack(logical_basis(code))
    generator = np.einsum("i,ijk->jk", axis, PAULIS)
    _, eigenvectors = np.linalg.eigh(generator)
    n_plus, n_minus = eigenvectors[:, 1], eigenvectors[:, 0]
    ket = pure_ket(vector)
    c_plus, c_minus = np.vdot(n_plus, ket), np.vdot(n_minus, ket)
    state = np.concatenate([c_plus*(encoding @ n_plus), c_minus*(encoding @ n_minus)])
    ops = logical_operators(code)
    logical_y = 1j*ops["X_L"] @ ops["Z_L"]
    hs = -OMEGA*(axis[0]*ops["X_L"] + axis[1]*logical_y + axis[2]*ops["Z_L"])
    return state, OMEGA*Z, hs, encoding


def legacy_weight(z, code):
    """Exact existing pairwise mappings on the repetition-code subspace."""
    z = np.clip(np.asarray(z, dtype=float), -1, 1)
    if code == "phaseflip":
        return 1+2*np.abs(z)
    if code != "bitflip":
        raise ValueError(code)
    p = (1+z)/2
    # Natural logarithm matches graph_mapping._von_neumann_entropy.
    term = lambda q: -q*np.log(np.clip(q, 1e-300, 1))
    return term(p)+term(1-p)


def occupation_spectrum(z):
    weights = (1+np.clip(np.asarray(z), -1, 1))/2
    lap = 3*np.eye(3)-np.ones((3, 3))
    return np.linalg.eigvalsh(weights[..., None, None]*lap)


def stable_minimum(costs):
    costs = np.asarray(costs)
    tolerance = 1e-12*max(1., abs(float(costs.min())))
    return int(np.flatnonzero(costs <= costs.min()+tolerance)[0])


def project_ball(vector):
    return vector/max(1., float(np.linalg.norm(vector)))


def estimate(means, weights, design, bank, code):
    """Estimator boundary: no true state, target density, or flip probability."""
    root = np.sqrt(weights)
    weighted_design = design*root[:, None]
    fitted, _, rank, _ = np.linalg.lstsq(weighted_design, means*root, rcond=1e-12)
    mixed = project_ball(fitted)
    spectrum = occupation_spectrum(means)
    reconstructed_means = spectrum.sum(axis=-1)/3-1
    spectral_fit = np.linalg.lstsq(weighted_design, reconstructed_means*root, rcond=1e-12)[0]
    spectral = project_ball(spectral_fit)
    norm = float(np.linalg.norm(fitted))
    pure = fitted/norm if rank == 3 and norm > 1e-12 else mixed.copy()
    bank_means = bank @ design.T
    denom = max(1., float(weights.sum()))
    raw_cost = np.sum(weights*(bank_means-means)**2, axis=1)/denom
    # ||(0,3w,3w)-(0,3v,3v)||^2 = 18*(w-v)^2.
    legacy_cost = 18*np.sum(weights*(legacy_weight(bank_means, code)
                                      -legacy_weight(means, code))**2, axis=1)/denom
    raw_index, legacy_index = stable_minimum(raw_cost), stable_minimum(legacy_cost)
    predictions = np.array([mixed, spectral, pure, bank[raw_index], bank[legacy_index]])
    return predictions, int(rank), {"raw": raw_index, "legacy": legacy_index}


def make_dataset():
    def directions(seed, count):
        values = np.random.default_rng(seed).normal(size=(count, 3))
        return values/np.linalg.norm(values, axis=1, keepdims=True)
    bank_positive = directions(2026092701, 16)
    test_positive = directions(2026092702, 32)
    bank = np.stack([bank_positive, -bank_positive], axis=1).reshape(-1, 3)
    targets = np.stack([test_positive, -test_positive], axis=1)
    max_overlap = float(np.max((1+targets.reshape(-1, 3) @ bank.T)/2))
    assert max_overlap < 1-1e-12
    return {"reference_seed": 2026092701, "test_seed": 2026092702,
            "bank": bank.tolist(), "target_pairs": targets.tolist(),
            "max_test_reference_fidelity": max_overlap, "measurement_seeds": list(range(12))}


def qualify(dataset):
    from ..core.clock import clock_state
    from ..core.graph_mapping import adjacency_from_reduced_density
    from ..core.laplacian import graph_laplacian, ordered_spectrum
    from ..core.relative_state import relative_state_density
    plus = np.ones(2)/np.sqrt(2)
    clock_states = [clock_state(OMEGA*Z, tau, plus) for tau in TAUS]
    effects = [np.outer(v, v.conj())/4 for v in clock_states]
    geometry = [float(1-abs(np.vdot(a, b))**2) for a, b in zip(clock_states, clock_states[1:])]
    bad_clock = [clock_state(OMEGA*Z, tau, np.array([1., 0.])) for tau in TAUS]
    maxima = defaultdict(float)
    details = {}
    bank = np.array(dataset["bank"])
    targets = np.array(dataset["target_pairs"]).reshape(-1, 3)
    for code, (axis_name, axis) in itertools.product(("bitflip", "phaseflip"), AXES.items()):
        design = measurement_design(axis)
        details[f"{code}_{axis_name}"] = {"design_rank": int(np.linalg.matrix_rank(design)),
            "singular_values": np.linalg.svd(design, compute_uv=False).tolist()}
        for vector in targets:
            state, hc, hs, encoding = history_state(vector, code, axis)
            total = np.kron(hc, np.eye(8))+np.kron(np.eye(2), hs)
            maxima["constraint_residual"] = max(maxima["constraint_residual"], float(np.linalg.norm(total @ state)))
            rho = np.outer(state, state.conj())
            for k, tau in enumerate(TAUS):
                actual = relative_state_density(rho, clock_states[k], 2, 8)
                u = logical_unitary(axis, tau)
                expected = encoding @ u @ bloch_density(vector) @ u.conj().T @ encoding.conj().T
                maxima["conditional_evolution_gap"] = max(maxima["conditional_evolution_gap"], float(np.linalg.norm(actual-expected)))
                probability = float(np.trace(np.kron(effects[k], np.eye(8)) @ rho).real)
                maxima["clock_probability_error"] = max(maxima["clock_probability_error"], abs(probability-1/8))
                mode = "mutual_info" if code == "bitflip" else "coherence_abs"
                spectrum = ordered_spectrum(graph_laplacian(adjacency_from_reduced_density(actual, 3, mode)))
                predicted = np.array([0., 3., 3.])*legacy_weight(design[k] @ vector, code)
                maxima["legacy_formula_gap"] = max(maxima["legacy_formula_gap"], float(np.linalg.norm(spectrum-predicted)))
            values = design @ vector
            maxima["legacy_antipodal_gap"] = max(maxima["legacy_antipodal_gap"],
                float(np.max(np.abs(legacy_weight(values, code)-legacy_weight(-values, code)))))
            predictions, rank, _ = estimate(values, np.ones(8), design, bank, code)
            maxima["raw_occupation_prediction_gap"] = max(maxima["raw_occupation_prediction_gap"],
                                                         float(np.linalg.norm(predictions[0]-predictions[1])))
            if axis_name == "tilted":
                maxima["noiseless_tilted_infidelity"] = max(maxima["noiseless_tilted_infidelity"],
                    float(1-(1+predictions[0] @ vector)/2))
    povm_gap = float(np.linalg.norm(sum(effects)-np.eye(2)))
    degenerate_geometry = max(1-abs(np.vdot(a, b))**2 for a, b in zip(bad_clock, bad_clock[1:]))
    checks = {"residuals_below_1e_minus_10": all(value < 1e-10 for value in maxima.values()),
        "povm_complete": povm_gap < 1e-10, "nondegenerate_clock": min(geometry) > .1,
        "degenerate_clock_negative_control": abs(degenerate_geometry) < 1e-10,
        "ranks_correct": all(v["design_rank"] == (3 if "tilted" in k else 1) for k, v in details.items())}
    checks = {key: bool(value) for key, value in checks.items()}
    return {"passed": all(checks.values()), "checks": checks, "maxima": dict(maxima),
        "models": details, "clock_adjacent_geometry": geometry,
        "povm_completeness_gap": povm_gap, "degenerate_clock_max_geometry": float(degenerate_geometry)}


def make_jobs():
    jobs = []
    for code, axis, copies, retained, flip, seed in itertools.product(
            ("bitflip", "phaseflip"), AXES, (128, 512, 2048), (1, 4, 8), (0., .05, .15), range(12)):
        job = {"code": code, "axis": axis, "copies": copies, "retained_labels": retained,
               "readout_flip": flip, "measurement_seed": seed}
        job["key"] = f"{code}_{axis}_n{copies}_k{retained}_q{flip:.2f}_s{seed:02d}"
        jobs.append(job)
    return jobs


def evaluate_job(job, dataset):
    targets = np.array(dataset["target_pairs"])
    bank = np.array(dataset["bank"])
    design = measurement_design(AXES[job["axis"]])
    rng = np.random.default_rng(np.random.SeedSequence([2026092703, list(AXES).index(job["axis"]),
        job["copies"], job["retained_labels"], int(round(100*job["readout_flip"])), job["measurement_seed"]]))
    fidelities, records = [], []
    ranks, accepted = [], []
    max_equivalence_gap = max_antipodal_gap = 0.
    for pair_id, pair in enumerate(targets):
        counts = rng.multinomial(job["copies"], np.ones(8)/8)
        keep = np.zeros(8, dtype=bool)
        keep[rng.choice(8, size=job["retained_labels"], replace=False)] = True
        true_means = design @ pair[0]
        prob = np.clip((1+(1-2*job["readout_flip"])*true_means)/2, 0, 1)
        successes = rng.binomial(counts, prob)
        measured = np.divide(2*successes, counts, out=np.ones(8), where=counts > 0)-1
        weights = counts*keep
        pair_predictions, pair_fidelity, selections = [], [], []
        for sign in (1, -1):
            predictions, rank, indexes = estimate(sign*measured, weights, design, bank, job["code"])
            # Target is used only after the estimator returns.
            pair_predictions.append(predictions)
            pair_fidelity.append(np.clip((1+predictions @ (sign*pair[0]))/2, 0, 1).tolist())
            selections.append(indexes)
            max_equivalence_gap = max(max_equivalence_gap, float(np.linalg.norm(predictions[0]-predictions[1])))
        max_antipodal_gap = max(max_antipodal_gap, float(np.linalg.norm(pair_predictions[0][-1]-pair_predictions[1][-1])))
        assert max_equivalence_gap < 1e-10 and max_antipodal_gap < 1e-10
        fidelities.append(pair_fidelity)
        ranks.append(rank)
        accepted.append(int(weights.sum()))
        records.append({"pair_id": pair_id, "counts_all_labels": counts.tolist(),
            "successes_positive_target": successes.tolist(), "retained_mask": keep.tolist(),
            "rank": rank, "reference_indices": selections})
    fids = np.array(fidelities)
    assert np.max(np.abs(fids[:, :, -1].mean(axis=1)-.5)) < 1e-10
    return {**job, "methods": METHODS, "fidelities_by_pair_sign_method": fidelities,
        "measurement_records": records, "rank_deficient_pairs": sum(rank < 3 for rank in ranks),
        "accepted_copies_mean": float(np.mean(accepted)), "prepared_copies_per_target": job["copies"],
        "max_raw_occupation_prediction_gap": max_equivalence_gap,
        "max_legacy_antipodal_prediction_gap": max_antipodal_gap}


def summarize(results, pilot):
    grouped = defaultdict(list)
    for result in results:
        key = (result["code"], result["axis"], result["copies"], result["retained_labels"], result["readout_flip"])
        grouped[key].append(result)
    summaries = []
    indices = np.random.default_rng(2026092704).integers(32, size=(5000, 32))
    for key, members in sorted(grouped.items()):
        values = np.array([m["fidelities_by_pair_sign_method"] for m in members])
        pair_mean = values.mean(axis=(0, 2))
        point = pair_mean.mean(axis=0)
        bootstrap = pair_mean[indices].mean(axis=1)
        intervals = np.quantile(bootstrap, [.025, .975], axis=0)
        differences = bootstrap-bootstrap[:, 0, None]
        difference_intervals = np.quantile(differences, [.025, .975], axis=0)
        summaries.append({"code": key[0], "axis": key[1], "copies": key[2], "retained_labels": key[3],
            "readout_flip": key[4], "measurement_seed_count": len(members), "pilot": pilot,
            "target_pairs": 32, "bootstrap_draws": 5000,
            "bootstrap_scope": "target-pair clusters after averaging fixed measurement seeds; paired methods",
            "rank_deficient_rate": sum(m["rank_deficient_pairs"] for m in members)/(32*len(members)),
            "accepted_copies_mean": float(np.mean([m["accepted_copies_mean"] for m in members])),
            "policies": {name: {"mean_fidelity": float(point[i]), "ci95": intervals[:, i].tolist(),
                "q05_fidelity": float(np.quantile(values[..., i], .05)),
                "difference_vs_raw_mixed": {"estimate": float(point[i]-point[0]),
                                           "ci95": difference_intervals[:, i].tolist()}}
                for i, name in enumerate(METHODS)}})
    return summaries


def report_markdown(summary, qualification, dataset, pilot):
    lines = ["# R1: finite-clock identifiability experiment", "",
        f"Run type: {'PILOT — not a full-grid result' if pilot else 'FULL GRID'}. "
        f"Physical/representation qualification passed: {qualification['passed']}.", "",
        "This is multi-copy state estimation with a known engineered logical Hamiltonian. "
        "The tilted Hamiltonian includes a three-body logical Pauli term. It is not the submitted H_S=0 "
        "model, not a physical-noise recovery channel, and not a C3R efficacy experiment.", "",
        "## Physical checks", "",
        f"- Max null-constraint residual: {qualification['maxima']['constraint_residual']:.5g}.",
        f"- Max conditional-evolution density gap: {qualification['maxima']['conditional_evolution_gap']:.5g}.",
        f"- Adjacent clock geometry minimum: {min(qualification['clock_adjacent_geometry']):.8f}.",
        f"- POVM completeness error: {qualification['povm_completeness_gap']:.5g}.",
        "- Measurement-design ranks: aligned 1; tilted 3. The clock labels are nonorthogonal POVM outcomes, not eight orthogonal ticks.",
        f"- Maximum test/reference fidelity: {dataset['max_test_reference_fidelity']:.8f}; no test state is in the bank.", "",
        "## Fixed display slice: all 8 labels, zero readout error", "",
        "All grid cells, intervals, q05 fidelity and resource counts are in summary.json. "
        "These are initial-state fidelities; known unitary evolution preserves this fidelity for the corresponding trajectories.", "",
        "| Code | Dynamics | Copies | Raw mixed LS [95% CI] | Occupation spectral LS | Raw pure LS | Raw nearest | Legacy spectral nearest |",
        "|---|---|---:|---|---:|---:|---:|---:|"]
    for s in summary:
        if s["retained_labels"] != 8 or s["readout_flip"] != 0:
            continue
        p = s["policies"]
        raw = p["raw_mixed_ls"]
        remaining = " | ".join(f"{p[k]['mean_fidelity']:.6f}" for k in METHODS[1:])
        lines.append(f"| {s['code']} | {s['axis']} | {s['copies']} | {raw['mean_fidelity']:.6f} "
            f"[{raw['ci95'][0]:.6f}, {raw['ci95'][1]:.6f}] | {remaining} |")
    lines += ["", "## What this can and cannot establish", "",
        "The original mutual-information/coherence-absolute representations lose the antipodal sign. "
        "Under the declared complementary-shot coupling, their pair-averaged fidelity is exactly 0.5. "
        "The zero-width interval here is a constructed identifiability control, not a population-risk guarantee.", "",
        "Occupation spectrum is an invertible encoding of the same signed population data, and must agree "
        "with raw mixed LS. Its benefit over legacy features is not a spectral advantage over equal-information "
        "estimation. Pure LS additionally uses the known-pure-state prior, so any advantage of that method "
        "must not be attributed to spectral processing.", "",
        "Confidence intervals resample 32 independent target pairs after averaging the fixed measurement seeds. "
        "The two codes are basis-equivalent coupled checks, not independent replication. Prepared-copy cost "
        "includes all clock-label erasures. Rank-deficient and zero-count cases are retained.", "",
        "A successful R1 qualifies a physical/observation model for a later recovery study; it does not repair "
        "the original spectral gate or validate C3R. No threshold was tuned on these test targets.", "",
        "Design references: [Page–Wootters constraints and conditioning](https://www.nature.com/articles/s41467-021-21782-4), "
        "[reduced-state identifiability](https://arxiv.org/abs/quant-ph/0207109). "
        "Numerical findings and the finite-clock construction above are from this local experiment.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=6, choices=range(1, 7))
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--preflight-only", action="store_true")
    args = parser.parse_args()
    if args.limit < 0:
        parser.error("limit must be non-negative")
    if args.output.exists():
        parser.error("Use a new directory; never overwrite an experiment")
    args.output.mkdir(parents=True)
    started = time.perf_counter()
    try:
        import scipy
        dataset = make_dataset()
        jobs = make_jobs()
        if args.limit:
            jobs = [jobs[i] for i in np.linspace(0, len(jobs)-1, min(args.limit, len(jobs)), dtype=int)]
        manifest = {"created_utc": datetime.now(timezone.utc).isoformat(), "python": sys.version,
            "numpy": np.__version__, "scipy": scipy.__version__, "workers": args.workers,
            "pilot": bool(args.limit), "preflight_only": args.preflight_only,
            "jobs": len(jobs), "target_rows": len(jobs)*64, "methods": METHODS,
            "protocol_sha256": sha256(PROTOCOL_PATH), "omega": OMEGA, "taus": TAUS.tolist(),
            "source_sha256": {str(p.relative_to(REPO_ROOT)): sha256(p)
                for p in (REPO_ROOT/"biqmn").rglob("*.py")},
            "limits": "Known engineered logical Hamiltonian includes 3-body term. Multi-copy estimation, no physical data noise, no C3R/QEC claim. Antipodal and code records coupled; not independent replicates."}
        write_json(args.output/"manifest.json", manifest)
        write_json(args.output/"dataset.json", dataset)
        write_json(args.output/"jobs.json", jobs)
        qualification = qualify(dataset)
        write_json(args.output/"qualification.json", qualification)
        if not qualification["passed"]:
            raise ValueError("Qualification failed; do not start a performance run")
        if args.preflight_only:
            write_json(args.output/"DONE.json", {"state": "qualified", "elapsed_seconds": time.perf_counter()-started})
            print(json.dumps(qualification, indent=2))
            return
        results = []
        def status(state):
            elapsed = time.perf_counter()-started
            value = {"state": state, "completed": len(results), "total": len(jobs),
                "target_rows_completed": len(results)*64, "elapsed_seconds": elapsed,
                "estimated_remaining_seconds": elapsed*(len(jobs)-len(results))/len(results) if results else None,
                "updated_utc": datetime.now(timezone.utc).isoformat()}
            write_json(args.output/"status.json", value)
            return value
        status("running")
        with (args.output/"job_results.jsonl").open("w", encoding="utf-8") as stream:
            with ProcessPoolExecutor(max_workers=args.workers) as pool:
                futures = [pool.submit(evaluate_job, job, dataset) for job in jobs]
                for future in as_completed(futures):
                    result = future.result()
                    results.append(result)
                    stream.write(json.dumps(result, allow_nan=False)+"\n")
                    stream.flush()
                    if len(results) % 24 == 0 or len(results) == len(jobs):
                        print(json.dumps(status("running")), flush=True)
        summary = summarize(results, bool(args.limit))
        write_json(args.output/"summary.json", summary)
        (args.output/"REPORT.md").write_text(report_markdown(summary, qualification, dataset, bool(args.limit)), encoding="utf-8")
        write_json(args.output/"DONE.json", status("completed"))
        print("COMPLETE", flush=True)
    except BaseException as exc:
        failure = {"state": "failed", "error": repr(exc), "traceback": traceback.format_exc()}
        write_json(args.output/"FAILED.json", failure)
        write_json(args.output/"status.json", failure)
        raise


if __name__ == "__main__":
    main()
