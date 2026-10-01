"""R2: held-out finite-clock template-switching risk experiment.

This is deliberately a multi-copy restoration decision study, not a generic
unknown-state QEC-channel claim.  See manuscript/revision_r2_protocol.md.
"""
from __future__ import annotations

import argparse
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
from .revision_audit import sha256
from .revision_identifiability import AXES, PAULIS, TAUS, bloch_density, logical_unitary, project_ball

POLICIES = ("a_continuous", "b_template", "c2_score", "u_uncertainty", "s_structural", "c3r")
PROTOCOL_PATH = REPO_ROOT.parent / "manuscript" / "revision_r2_protocol.md"


def _directions(seed: int, count: int) -> np.ndarray:
    values = np.random.default_rng(seed).normal(size=(count, 3))
    return values / np.linalg.norm(values, axis=1, keepdims=True)


def make_dataset() -> dict:
    bank_positive = _directions(2026092701, 16)
    calibration_positive = _directions(2026092711, 16)
    test_positive = _directions(2026092712, 32)
    bank = np.stack([bank_positive, -bank_positive], axis=1).reshape(-1, 3)
    calibration = np.stack([calibration_positive, -calibration_positive], axis=1)
    targets = np.stack([test_positive, -test_positive], axis=1)
    all_test = targets.reshape(-1, 3)
    assert float(np.max((1 + all_test @ bank.T) / 2)) < 1 - 1e-12
    assert float(np.max((1 + all_test @ calibration.reshape(-1, 3).T) / 2)) < 1 - 1e-12
    return {
        "reference_seed": 2026092701,
        "calibration_seed": 2026092711,
        "test_seed": 2026092712,
        "bank": bank.tolist(),
        "calibration_pairs": calibration.tolist(),
        "test_pairs": targets.tolist(),
    }


def _kron3(local: np.ndarray, bits: tuple[int, int, int]) -> np.ndarray:
    factors = [local if bit else np.eye(2, dtype=complex) for bit in bits]
    return np.kron(np.kron(factors[0], factors[1]), factors[2])


def physical_measurement_design(code: str, axis: np.ndarray, noise: float) -> np.ndarray:
    """Map an initial logical Bloch vector to noisy logical-Z means at each clock label."""
    from ..core.encoding import logical_basis, logical_operators

    if code not in {"bitflip", "phaseflip"}:
        raise ValueError(code)
    if not 0 <= noise <= 1:
        raise ValueError("physical noise must be in [0, 1]")
    encoding = np.column_stack(logical_basis(code))
    z_logical = logical_operators(code)["Z_L"]
    local = PAULIS[0] if code == "bitflip" else PAULIS[2]
    kraus = []
    for bits in itertools.product((0, 1), repeat=3):
        weight = sum(bits)
        probability = noise ** weight * (1 - noise) ** (3 - weight)
        kraus.append((probability, _kron3(local, bits)))
    design = np.empty((len(TAUS), 3), dtype=float)
    for row, tau in enumerate(TAUS):
        unitary = logical_unitary(axis, tau)
        for col in range(3):
            vector = np.zeros(3)
            vector[col] = 1.0
            rho = encoding @ unitary @ bloch_density(vector) @ unitary.conj().T @ encoding.conj().T
            noisy = sum(probability * op @ rho @ op.conj().T for probability, op in kraus)
            design[row, col] = float(np.trace(z_logical @ noisy).real)
    return design


def _fit(means: np.ndarray, weights: np.ndarray, design: np.ndarray) -> tuple[np.ndarray, float]:
    root = np.sqrt(weights)
    fitted, _, _, _ = np.linalg.lstsq(design * root[:, None], means * root, rcond=1e-12)
    candidate = project_ball(fitted)
    denom = max(float(weights.sum()), 1.0)
    loss = float(np.sum(weights * (design @ candidate - means) ** 2) / denom)
    return candidate, loss


def _nearest_template(means: np.ndarray, weights: np.ndarray, design: np.ndarray, bank: np.ndarray) -> tuple[np.ndarray, int, float]:
    denom = max(float(weights.sum()), 1.0)
    costs = np.sum(weights[None, :] * (bank @ design.T - means[None, :]) ** 2, axis=1) / denom
    tolerance = 1e-12 * max(1.0, abs(float(costs.min())))
    index = int(np.flatnonzero(costs <= costs.min() + tolerance)[0])
    return bank[index].copy(), index, float(costs[index])


def _draw_record(vector: np.ndarray, rng: np.random.Generator, design: np.ndarray, bank: np.ndarray,
                 copies: int, readout_flip: float, thresholds: dict | None) -> dict:
    """Generate a coupled antipodal pair; target is used only in returned evaluator fields."""
    counts = rng.multinomial(copies, np.full(len(TAUS), 1 / len(TAUS)))
    fitting = np.zeros(len(TAUS), dtype=bool)
    fitting[rng.choice(len(TAUS), size=4, replace=False)] = True
    validation = ~fitting
    positive_mean = design @ vector
    probability = np.clip((1 + (1 - 2 * readout_flip) * positive_mean) / 2, 0, 1)
    successes = rng.binomial(counts, probability)
    observed_positive = np.divide(2 * successes, counts, out=np.zeros_like(positive_mean), where=counts > 0) - 1
    corrected_positive = np.clip(observed_positive / max(1 - 2 * readout_flip, 1e-12), -1, 1)
    records = []
    for sign in (1, -1):
        means = sign * corrected_positive
        fit_weights = counts * fitting
        val_weights = counts * validation
        a, fit_a = _fit(means, fit_weights, design)
        b, bank_index, fit_b = _nearest_template(means, fit_weights, design, bank)
        _, val_a = _fit(means, val_weights, design)
        val_b = float(np.sum(val_weights * (design @ b - means) ** 2) / max(float(val_weights.sum()), 1.0))
        gram = design.T @ (fit_weights[:, None] * design)
        uncertainty = float(np.sqrt(np.trace(np.linalg.pinv(gram, rcond=1e-12))))
        score = fit_b - fit_a
        structural = val_b - val_a
        if thresholds is None:
            decision = {}
        else:
            proposal = score <= thresholds["score_max"]
            uncertainty_ok = uncertainty <= thresholds["uncertainty_max"]
            structural_ok = structural <= thresholds["structural_max"]
            decision = {
                "c2_score": proposal,
                "u_uncertainty": proposal and uncertainty_ok,
                "s_structural": proposal and structural_ok,
                "c3r": proposal and uncertainty_ok and structural_ok,
                "proposal": proposal,
                "uncertainty_ok": uncertainty_ok,
                "structural_ok": structural_ok,
            }
        target = sign * vector
        fidelity_a = float(np.clip((1 + a @ target) / 2, 0, 1))
        fidelity_b = float(np.clip((1 + b @ target) / 2, 0, 1))
        records.append({
            "sign": sign, "fit_mask": fitting.tolist(), "counts": counts.tolist(),
            "bank_index": bank_index, "score": score, "uncertainty": uncertainty, "structural": structural,
            "fidelity_a": fidelity_a, "fidelity_b": fidelity_b, "decision": decision,
        })
    return records


def calibrate(dataset: dict) -> dict:
    """Set all gate thresholds before touching held-out targets."""
    bank = np.asarray(dataset["bank"], dtype=float)
    pairs = np.asarray(dataset["calibration_pairs"], dtype=float)
    design = physical_measurement_design("bitflip", AXES["tilted"], 0.05)
    values = {"score": [], "uncertainty": [], "structural": []}
    for measurement_seed in range(12):
        for pair_id, pair in enumerate(pairs):
            rng = np.random.default_rng(np.random.SeedSequence([2026092713, measurement_seed, pair_id]))
            for row in _draw_record(pair[0], rng, design, bank, 1024, 0.05, None):
                for key in values:
                    values[key].append(float(row[key]))
    return {
        "calibration_operating_point": {"code": "bitflip", "axis": "tilted", "copies": 1024,
                                          "physical_noise": 0.05, "readout_flip": 0.05},
        "score_max": float(np.quantile(values["score"], .75)),
        "uncertainty_max": float(np.quantile(values["uncertainty"], .75)),
        "structural_max": float(np.quantile(values["structural"], .75)),
        "quantiles": {"score": .75, "uncertainty": .75, "structural": .75},
        "calibration_records": len(values["score"]),
    }


def make_jobs() -> list[dict]:
    jobs = []
    for code, copies, physical_noise, readout_flip, measurement_seed in itertools.product(
            ("bitflip", "phaseflip"), (256, 1024), (0.01, 0.05, 0.10), (0.0, 0.05), range(12)):
        jobs.append({"code": code, "axis": "tilted", "copies": copies, "physical_noise": physical_noise,
                     "readout_flip": readout_flip, "measurement_seed": measurement_seed})
    return jobs


def evaluate_job(job: dict, dataset: dict, thresholds: dict) -> dict:
    bank = np.asarray(dataset["bank"], dtype=float)
    targets = np.asarray(dataset["test_pairs"], dtype=float)
    design = physical_measurement_design(job["code"], AXES[job["axis"]], job["physical_noise"])
    records = []
    for pair_id, pair in enumerate(targets):
        seed = [2026092714, 0 if job["code"] == "bitflip" else 1, job["copies"],
                int(100 * job["physical_noise"]), int(100 * job["readout_flip"]), job["measurement_seed"], pair_id]
        rng = np.random.default_rng(np.random.SeedSequence(seed))
        for record in _draw_record(pair[0], rng, design, bank, job["copies"], job["readout_flip"], thresholds):
            record["pair_id"] = pair_id
            records.append(record)
    return {**job, "records": records, "design_rank": int(np.linalg.matrix_rank(design))}


def _policy_record(row: dict, policy: str) -> tuple[float, bool, bool]:
    if policy == "a_continuous":
        return row["fidelity_a"], False, False
    if policy == "b_template":
        switched = True
    else:
        switched = bool(row["decision"][policy])
    fidelity = row["fidelity_b"] if switched else row["fidelity_a"]
    harmful = bool(switched and row["fidelity_b"] < row["fidelity_a"] - 1e-12)
    return fidelity, switched, harmful


def summarize(results: list[dict], pilot: bool) -> list[dict]:
    grouped: dict[tuple, list[dict]] = {}
    for result in results:
        key = tuple(result[name] for name in ("code", "copies", "physical_noise", "readout_flip"))
        grouped.setdefault(key, []).append(result)
    summary = []
    bootstrap_rng = np.random.default_rng(2026092715)
    for key, members in sorted(grouped.items()):
        members.sort(key=lambda item: item["measurement_seed"])
        per_seed = []
        switches, harmful = [], []
        for member in members:
            pair_values, pair_switches, pair_harmful = [], [], []
            for pair_id in range(32):
                signs = [row for row in member["records"] if row["pair_id"] == pair_id]
                pair_values.append([np.mean([_policy_record(row, policy)[0] for row in signs]) for policy in POLICIES])
                pair_switches.append([np.mean([_policy_record(row, policy)[1] for row in signs]) for policy in POLICIES])
                pair_harmful.append([np.mean([_policy_record(row, policy)[2] for row in signs]) for policy in POLICIES])
            per_seed.append(pair_values)
            switches.append(pair_switches)
            harmful.append(pair_harmful)
        values = np.asarray(per_seed).mean(axis=0)
        indices = bootstrap_rng.integers(32, size=(2000 if pilot else 5000, 32))
        boot = values[indices].mean(axis=1)
        switch_values = np.asarray(switches).mean(axis=0)
        harmful_values = np.asarray(harmful).mean(axis=0)
        switch_mean = switch_values.mean(axis=0)
        harmful_mean = harmful_values.mean(axis=0)
        harmful_boot = harmful_values[indices].mean(axis=1)
        c2_index, u_index, a_index = (POLICIES.index(name) for name in ("c2_score", "u_uncertainty", "a_continuous"))
        policies = {}
        for index, policy in enumerate(POLICIES):
            policies[policy] = {
                "mean_fidelity": float(values[:, index].mean()),
                "ci95": np.quantile(boot[:, index], [.025, .975]).tolist(),
                "mean_fidelity_difference_vs_a": {
                    "estimate": float(values[:, index].mean() - values[:, a_index].mean()),
                    "ci95": np.quantile(boot[:, index] - boot[:, a_index], [.025, .975]).tolist(),
                },
                "q05_fidelity": float(np.quantile(values[:, index], .05)),
                "cvar05_exact_mass": float(np.sort(values[:, index])[:2].mean()),
                "switch_rate": float(switch_mean[index]),
                "false_safe_rate": float(harmful_mean[index]),
                "false_safe_ci95": np.quantile(harmful_boot[:, index], [.025, .975]).tolist(),
                "false_safe_difference_vs_c2": {
                    "estimate": float(harmful_mean[index] - harmful_mean[c2_index]),
                    "ci95": np.quantile(harmful_boot[:, index] - harmful_boot[:, c2_index], [.025, .975]).tolist(),
                },
                "false_safe_difference_vs_u": {
                    "estimate": float(harmful_mean[index] - harmful_mean[u_index]),
                    "ci95": np.quantile(harmful_boot[:, index] - harmful_boot[:, u_index], [.025, .975]).tolist(),
                },
            }
        summary.append({"code": key[0], "copies": key[1], "physical_noise": key[2],
                        "readout_flip": key[3], "measurement_seed_count": len(members),
                        "pilot": pilot, "design_rank": members[0]["design_rank"], "policies": policies})
    return summary


def report_markdown(summary: list[dict], thresholds: dict, pilot: bool) -> str:
    lines = ["# R2: held-out finite-clock template-switching risk test", "",
             f"Run type: {'PILOT — not a confirmatory result' if pilot else 'FULL GRID'}.", "",
             "This is a multi-copy restoration/decision test, not a generic QEC channel test. "
             "Thresholds were set on a disjoint calibration set before evaluating held-out targets.", "",
             "## Fixed calibration", "",
             f"- score maximum: {thresholds['score_max']:.8g}",
             f"- uncertainty maximum: {thresholds['uncertainty_max']:.8g}",
             f"- structural validation-residual maximum: {thresholds['structural_max']:.8g}", "",
             "## Policy summary", "",
             "| Code | Copies | Physical noise | Readout flip | Policy | Mean fidelity [95% CI] | q05 | CVaR05 | Switch rate | False-safe rate |",
             "|---|---:|---:|---:|---|---|---:|---:|---:|---:|"]
    for cell in summary:
        for policy, data in cell["policies"].items():
            ci = data["ci95"]
            lines.append(f"| {cell['code']} | {cell['copies']} | {cell['physical_noise']:.2f} | "
                         f"{cell['readout_flip']:.2f} | {policy} | {data['mean_fidelity']:.6f} "
                         f"[{ci[0]:.6f}, {ci[1]:.6f}] | {data['q05_fidelity']:.6f} | "
                         f"{data['cvar05_exact_mass']:.6f} | {data['switch_rate']:.4f} | {data['false_safe_rate']:.4f} |")
    lines += ["", "## Interpretation boundary", "",
              "A distinct structural contribution requires nonzero structural-only blocking and a lower false-safe "
              "rate than score-only after comparison with uncertainty-only.  If that pattern is absent, the "
              "manuscript must retain the uncertainty-control interpretation stated in the protocol.", ""]
    lines += ["## Paired gate comparisons", "",
              "Differences are policy-minus-baseline rates, in percentage points; intervals resample the 32 target pairs after averaging measurement seeds.", "",
              "| Code | Copies | Physical noise | Readout flip | S minus C2 false-safe [95% CI] | C3R minus U false-safe [95% CI] | C3R minus A fidelity [95% CI] |",
              "|---|---:|---:|---:|---|---|---|"]
    for cell in summary:
        s = cell["policies"]["s_structural"]["false_safe_difference_vs_c2"]
        c3 = cell["policies"]["c3r"]["false_safe_difference_vs_u"]
        fidelity = cell["policies"]["c3r"]["mean_fidelity_difference_vs_a"]
        lines.append(f"| {cell['code']} | {cell['copies']} | {cell['physical_noise']:.2f} | {cell['readout_flip']:.2f} | "
                     f"{100*s['estimate']:.3f} [{100*s['ci95'][0]:.3f}, {100*s['ci95'][1]:.3f}] | "
                     f"{100*c3['estimate']:.3f} [{100*c3['ci95'][0]:.3f}, {100*c3['ci95'][1]:.3f}] | "
                     f"{fidelity['estimate']:.6f} [{fidelity['ci95'][0]:.6f}, {fidelity['ci95'][1]:.6f}] |")
    lines += [""]
    return "\n".join(lines)


def _write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=6, choices=range(1, 7))
    parser.add_argument("--limit", type=int, default=0, help="Run evenly spaced pilot jobs; never use as final evidence.")
    args = parser.parse_args()
    if args.limit < 0:
        parser.error("limit must be non-negative")
    if args.output.exists():
        parser.error("Output exists; R2 never overwrites a run.")
    args.output.mkdir(parents=True)
    started = time.perf_counter()
    try:
        import scipy
        dataset = make_dataset()
        thresholds = calibrate(dataset)
        jobs = make_jobs()
        pilot = bool(args.limit)
        if pilot:
            jobs = [jobs[index] for index in np.linspace(0, len(jobs) - 1, min(args.limit, len(jobs)), dtype=int)]
        manifest = {"created_utc": datetime.now(timezone.utc).isoformat(), "python": sys.version,
                    "numpy": np.__version__, "scipy": scipy.__version__, "workers": args.workers,
                    "pilot": pilot, "jobs": len(jobs), "target_states_per_job": 64,
                    "policies": POLICIES, "protocol_sha256": sha256(PROTOCOL_PATH),
                    "source_sha256": sha256(Path(__file__)), "limits": "Multi-copy restoration decision only; no generic QEC or spectral advantage claim."}
        _write_json(args.output / "manifest.json", manifest)
        _write_json(args.output / "dataset.json", dataset)
        _write_json(args.output / "thresholds.json", thresholds)
        results = []
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            futures = [executor.submit(evaluate_job, job, dataset, thresholds) for job in jobs]
            for future in as_completed(futures):
                results.append(future.result())
        results.sort(key=lambda item: (item["code"], item["copies"], item["physical_noise"], item["readout_flip"], item["measurement_seed"]))
        summary = summarize(results, pilot)
        _write_json(args.output / "results.json", results)
        _write_json(args.output / "summary.json", summary)
        (args.output / "REPORT.md").write_text(report_markdown(summary, thresholds, pilot), encoding="utf-8")
        _write_json(args.output / "DONE.json", {"state": "success", "seconds": time.perf_counter() - started})
    except Exception as error:
        _write_json(args.output / "FAILED.json", {"state": "failed", "error": repr(error),
                                                    "traceback": traceback.format_exc()})
        raise


if __name__ == "__main__":
    main()
