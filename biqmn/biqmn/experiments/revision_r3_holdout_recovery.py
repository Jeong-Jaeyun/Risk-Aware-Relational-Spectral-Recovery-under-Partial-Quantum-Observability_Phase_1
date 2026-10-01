"""R3: corrected held-out residual template-switching experiment.

R3 preserves R2 and evaluates a new, explicitly defined policy: candidates A
and B are fitted on fitting labels and both are scored unchanged on validation
labels.  See manuscript/revision_r3_protocol.md.
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

from . import revision_r2_recovery as r2
from .common import REPO_ROOT
from .revision_audit import sha256
from .revision_identifiability import AXES


POLICIES = (
    "a_continuous",
    "b_template",
    "c2_score",
    "u_uncertainty",
    "h_holdout_residual",
    "c3r",
)
PROTOCOL_PATH = REPO_ROOT.parent / "manuscript" / "revision_r3_protocol.md"
BOOTSTRAP_DRAWS = 5000


def make_dataset(replication: int) -> dict:
    """Create the fixed R3 dataset for one declared replication stream."""
    if replication < 0:
        raise ValueError("replication must be non-negative")
    if replication == 0:
        dataset = r2.make_dataset()
        dataset.update({
            "replication": 0,
            "calibration_measurement_seed": 2026092713,
            "test_measurement_seed": 2026092714,
        })
        return dataset

    base = 2026093000 + 100 * replication
    bank_positive = r2._directions(base + 1, 16)
    calibration_positive = r2._directions(base + 2, 16)
    test_positive = r2._directions(base + 3, 32)
    bank = np.stack([bank_positive, -bank_positive], axis=1).reshape(-1, 3)
    calibration = np.stack([calibration_positive, -calibration_positive], axis=1)
    targets = np.stack([test_positive, -test_positive], axis=1)
    all_test = targets.reshape(-1, 3)
    assert float(np.max((1 + all_test @ bank.T) / 2)) < 1 - 1e-12
    assert float(np.max((1 + all_test @ calibration.reshape(-1, 3).T) / 2)) < 1 - 1e-12
    return {
        "replication": replication,
        "reference_seed": base + 1,
        "calibration_seed": base + 2,
        "test_seed": base + 3,
        "calibration_measurement_seed": base + 4,
        "test_measurement_seed": base + 5,
        "bank": bank.tolist(),
        "calibration_pairs": calibration.tolist(),
        "test_pairs": targets.tolist(),
    }


def _weighted_loss(means: np.ndarray, weights: np.ndarray, design: np.ndarray,
                   candidate: np.ndarray) -> float:
    denominator = max(float(weights.sum()), 1.0)
    return float(np.sum(weights * (design @ candidate - means) ** 2) / denominator)


def _draw_record(vector: np.ndarray, rng: np.random.Generator, design: np.ndarray,
                 bank: np.ndarray, copies: int, readout_flip: float,
                 thresholds: dict | None) -> list[dict]:
    """Draw a coupled antipodal record; targets are evaluator-only fields."""
    counts = rng.multinomial(copies, np.full(len(r2.TAUS), 1 / len(r2.TAUS)))
    fitting = np.zeros(len(r2.TAUS), dtype=bool)
    fitting[rng.choice(len(r2.TAUS), size=4, replace=False)] = True
    validation = ~fitting
    positive_mean = design @ vector
    probability = np.clip((1 + (1 - 2 * readout_flip) * positive_mean) / 2, 0, 1)
    successes = rng.binomial(counts, probability)
    observed_positive = np.divide(
        2 * successes,
        counts,
        out=np.zeros_like(positive_mean),
        where=counts > 0,
    ) - 1
    corrected_positive = np.clip(
        observed_positive / max(1 - 2 * readout_flip, 1e-12),
        -1,
        1,
    )

    records = []
    for sign in (1, -1):
        means = sign * corrected_positive
        fit_weights = counts * fitting
        validation_weights = counts * validation
        a, fit_a = r2._fit(means, fit_weights, design)
        b, bank_index, fit_b = r2._nearest_template(means, fit_weights, design, bank)
        validation_loss_a = _weighted_loss(means, validation_weights, design, a)
        validation_loss_b = _weighted_loss(means, validation_weights, design, b)
        gram = design.T @ (fit_weights[:, None] * design)
        uncertainty = float(np.sqrt(np.trace(np.linalg.pinv(gram, rcond=1e-12))))
        score = fit_b - fit_a
        holdout_residual = validation_loss_b - validation_loss_a
        if thresholds is None:
            decision = {}
        else:
            proposal = score <= thresholds["score_max"]
            uncertainty_ok = uncertainty <= thresholds["uncertainty_max"]
            holdout_ok = holdout_residual <= thresholds["holdout_residual_max"]
            decision = {
                "c2_score": proposal,
                "u_uncertainty": proposal and uncertainty_ok,
                "h_holdout_residual": proposal and holdout_ok,
                "c3r": proposal and uncertainty_ok and holdout_ok,
                "proposal": proposal,
                "uncertainty_ok": uncertainty_ok,
                "holdout_ok": holdout_ok,
            }
        target = sign * vector
        fidelity_a = float(np.clip((1 + a @ target) / 2, 0, 1))
        fidelity_b = float(np.clip((1 + b @ target) / 2, 0, 1))
        oracle_template_fidelity = float(np.max((1 + bank @ target) / 2))
        records.append({
            "sign": sign,
            "fit_mask": fitting.tolist(),
            "counts": counts.tolist(),
            "bank_index": bank_index,
            "score": score,
            "uncertainty": uncertainty,
            "holdout_residual": holdout_residual,
            "validation_loss_a_fit": validation_loss_a,
            "validation_loss_b_fit": validation_loss_b,
            "fidelity_a": fidelity_a,
            "fidelity_b": fidelity_b,
            "oracle_template_fidelity": oracle_template_fidelity,
            "decision": decision,
        })
    return records


def calibrate(dataset: dict) -> dict:
    """Set every R3 threshold before evaluating any held-out target."""
    bank = np.asarray(dataset["bank"], dtype=float)
    pairs = np.asarray(dataset["calibration_pairs"], dtype=float)
    design = r2.physical_measurement_design("bitflip", AXES["tilted"], 0.05)
    values = {"score": [], "uncertainty": [], "holdout_residual": []}
    for measurement_seed in range(12):
        for pair_id, pair in enumerate(pairs):
            rng = np.random.default_rng(np.random.SeedSequence([
                dataset["calibration_measurement_seed"], measurement_seed, pair_id,
            ]))
            for row in _draw_record(pair[0], rng, design, bank, 1024, 0.05, None):
                for key in values:
                    values[key].append(float(row[key]))
    return {
        "calibration_operating_point": {
            "code": "bitflip",
            "axis": "tilted",
            "copies": 1024,
            "physical_noise": 0.05,
            "readout_flip": 0.05,
        },
        "score_max": float(np.quantile(values["score"], 0.75)),
        "uncertainty_max": float(np.quantile(values["uncertainty"], 0.75)),
        "holdout_residual_max": float(np.quantile(values["holdout_residual"], 0.75)),
        "quantiles": {"score": 0.75, "uncertainty": 0.75, "holdout_residual": 0.75},
        "calibration_records": len(values["score"]),
    }


def make_jobs() -> list[dict]:
    jobs = []
    for code, copies, physical_noise, readout_flip, measurement_seed in itertools.product(
            ("bitflip", "phaseflip"),
            (256, 1024),
            (0.01, 0.05, 0.10),
            (0.0, 0.05),
            range(12),
    ):
        jobs.append({
            "code": code,
            "axis": "tilted",
            "copies": copies,
            "physical_noise": physical_noise,
            "readout_flip": readout_flip,
            "measurement_seed": measurement_seed,
        })
    return jobs


def evaluate_job(job: dict, dataset: dict, thresholds: dict) -> dict:
    bank = np.asarray(dataset["bank"], dtype=float)
    targets = np.asarray(dataset["test_pairs"], dtype=float)
    design = r2.physical_measurement_design(job["code"], AXES[job["axis"]], job["physical_noise"])
    records = []
    for pair_id, pair in enumerate(targets):
        seed = [
            dataset["test_measurement_seed"],
            0 if job["code"] == "bitflip" else 1,
            job["copies"],
            int(100 * job["physical_noise"]),
            int(100 * job["readout_flip"]),
            job["measurement_seed"],
            pair_id,
        ]
        rng = np.random.default_rng(np.random.SeedSequence(seed))
        for record in _draw_record(pair[0], rng, design, bank, job["copies"],
                                   job["readout_flip"], thresholds):
            record["pair_id"] = pair_id
            records.append(record)
    return {**job, "records": records, "design_rank": int(np.linalg.matrix_rank(design))}


def _policy_record(row: dict, policy: str) -> tuple[float, bool, bool]:
    if policy == "a_continuous":
        return row["fidelity_a"], False, False
    switched = True if policy == "b_template" else bool(row["decision"][policy])
    fidelity = row["fidelity_b"] if switched else row["fidelity_a"]
    harmful = bool(switched and row["fidelity_b"] < row["fidelity_a"] - 1e-12)
    return fidelity, switched, harmful


def _two_way_indices(rng: np.random.Generator, seeds: int, pairs: int, draws: int) -> tuple[np.ndarray, np.ndarray]:
    return (
        rng.integers(seeds, size=(draws, seeds)),
        rng.integers(pairs, size=(draws, pairs)),
    )


def _two_way_means(values: np.ndarray, seed_indices: np.ndarray,
                   pair_indices: np.ndarray) -> np.ndarray:
    return values[seed_indices[:, :, None], pair_indices[:, None, :]].mean(axis=(1, 2))


def summarize(results: list[dict], pilot: bool) -> list[dict]:
    """Summarize with paired target-pair and measurement-seed resampling."""
    grouped: dict[tuple, list[dict]] = {}
    for result in results:
        key = tuple(result[name] for name in ("code", "copies", "physical_noise", "readout_flip"))
        grouped.setdefault(key, []).append(result)
    summary = []
    bootstrap_rng = np.random.default_rng(2026093006)
    draws = 2000 if pilot else BOOTSTRAP_DRAWS
    for key, members in sorted(grouped.items()):
        members.sort(key=lambda item: item["measurement_seed"])
        per_seed_values, per_seed_switches, per_seed_harmful, per_seed_oracle = [], [], [], []
        for member in members:
            pair_values, pair_switches, pair_harmful, pair_oracle = [], [], [], []
            for pair_id in range(32):
                signs = [row for row in member["records"] if row["pair_id"] == pair_id]
                if len(signs) != 2:
                    raise ValueError("each target pair must contain its two coupled signs")
                pair_values.append([
                    np.mean([_policy_record(row, policy)[0] for row in signs])
                    for policy in POLICIES
                ])
                pair_switches.append([
                    np.mean([_policy_record(row, policy)[1] for row in signs])
                    for policy in POLICIES
                ])
                pair_harmful.append([
                    np.mean([_policy_record(row, policy)[2] for row in signs])
                    for policy in POLICIES
                ])
                pair_oracle.append(np.mean([row["oracle_template_fidelity"] for row in signs]))
            per_seed_values.append(pair_values)
            per_seed_switches.append(pair_switches)
            per_seed_harmful.append(pair_harmful)
            per_seed_oracle.append(pair_oracle)

        values = np.asarray(per_seed_values, dtype=float)
        switches = np.asarray(per_seed_switches, dtype=float)
        harmful = np.asarray(per_seed_harmful, dtype=float)
        oracle = np.asarray(per_seed_oracle, dtype=float)[..., None]
        seed_indices, pair_indices = _two_way_indices(
            bootstrap_rng,
            values.shape[0],
            values.shape[1],
            draws,
        )
        boot_values = _two_way_means(values, seed_indices, pair_indices)
        boot_harmful = _two_way_means(harmful, seed_indices, pair_indices)
        boot_oracle = _two_way_means(oracle, seed_indices, pair_indices)[:, 0]
        mean_values = values.mean(axis=(0, 1))
        mean_switches = switches.mean(axis=(0, 1))
        mean_harmful = harmful.mean(axis=(0, 1))
        pair_mean_values = values.mean(axis=0)
        a_index = POLICIES.index("a_continuous")
        c2_index = POLICIES.index("c2_score")
        u_index = POLICIES.index("u_uncertainty")
        policies = {}
        for index, policy in enumerate(POLICIES):
            policies[policy] = {
                "mean_fidelity": float(mean_values[index]),
                "ci95_two_way": np.quantile(boot_values[:, index], [0.025, 0.975]).tolist(),
                "mean_fidelity_difference_vs_a": {
                    "estimate": float(mean_values[index] - mean_values[a_index]),
                    "ci95_two_way": np.quantile(
                        boot_values[:, index] - boot_values[:, a_index],
                        [0.025, 0.975],
                    ).tolist(),
                },
                "q05_fidelity": float(np.quantile(pair_mean_values[:, index], 0.05)),
                "cvar05_exact_mass": float(np.sort(pair_mean_values[:, index])[:2].mean()),
                "switch_rate": float(mean_switches[index]),
                "false_safe_rate": float(mean_harmful[index]),
                "false_safe_ci95_two_way": np.quantile(
                    boot_harmful[:, index],
                    [0.025, 0.975],
                ).tolist(),
                "false_safe_difference_vs_c2": {
                    "estimate": float(mean_harmful[index] - mean_harmful[c2_index]),
                    "ci95_two_way": np.quantile(
                        boot_harmful[:, index] - boot_harmful[:, c2_index],
                        [0.025, 0.975],
                    ).tolist(),
                },
                "false_safe_difference_vs_u": {
                    "estimate": float(mean_harmful[index] - mean_harmful[u_index]),
                    "ci95_two_way": np.quantile(
                        boot_harmful[:, index] - boot_harmful[:, u_index],
                        [0.025, 0.975],
                    ).tolist(),
                },
            }
        summary.append({
            "code": key[0],
            "copies": key[1],
            "physical_noise": key[2],
            "readout_flip": key[3],
            "measurement_seed_count": len(members),
            "target_pair_count": values.shape[1],
            "bootstrap": {
                "method": "two_way_cluster_bootstrap_target_pairs_and_measurement_seeds",
                "draws": draws,
                "conditional_on": "fixed_model_grid_and_calibration_set",
            },
            "pilot": pilot,
            "design_rank": members[0]["design_rank"],
            "oracle_direct_template_fidelity": {
                "mean": float(oracle.mean()),
                "ci95_two_way": np.quantile(boot_oracle, [0.025, 0.975]).tolist(),
                "policy_input": False,
            },
            "policies": policies,
        })
    return summary


def report_markdown(summary: list[dict], thresholds: dict, replication: int, pilot: bool) -> str:
    lines = [
        "# R3: corrected held-out residual template-switching test",
        "",
        f"Run type: {'PILOT -- not final evidence' if pilot else 'FULL GRID'}.",
        f"Replication: {replication}.",
        "",
        "Candidates A and B are fitted on fitting labels and scored unchanged on validation labels.",
        "Intervals are two-way cluster bootstrap intervals over target pairs and measurement seeds.",
        "This is multi-copy restoration/decision, not a QEC-channel or spectral-advantage test.",
        "",
        "## Fixed calibration",
        "",
        f"- score maximum: {thresholds['score_max']:.8g}",
        f"- uncertainty maximum: {thresholds['uncertainty_max']:.8g}",
        f"- held-out residual maximum: {thresholds['holdout_residual_max']:.8g}",
        "",
        "## Paired gate comparisons",
        "",
        "Differences are policy-minus-baseline rates, in percentage points; negative false-safe differences are favorable.",
        "",
        "| Code | Copies | Physical noise | Readout flip | H minus C2 false-safe [95% CI] | C3R minus U false-safe [95% CI] | C3R minus A fidelity [95% CI] | Oracle template fidelity |",
        "|---|---:|---:|---:|---|---|---|---|",
    ]
    for cell in summary:
        h = cell["policies"]["h_holdout_residual"]["false_safe_difference_vs_c2"]
        c3 = cell["policies"]["c3r"]["false_safe_difference_vs_u"]
        fidelity = cell["policies"]["c3r"]["mean_fidelity_difference_vs_a"]
        oracle = cell["oracle_direct_template_fidelity"]
        lines.append(
            f"| {cell['code']} | {cell['copies']} | {cell['physical_noise']:.2f} | "
            f"{cell['readout_flip']:.2f} | "
            f"{100 * h['estimate']:.3f} [{100 * h['ci95_two_way'][0]:.3f}, {100 * h['ci95_two_way'][1]:.3f}] | "
            f"{100 * c3['estimate']:.3f} [{100 * c3['ci95_two_way'][0]:.3f}, {100 * c3['ci95_two_way'][1]:.3f}] | "
            f"{fidelity['estimate']:.6f} [{fidelity['ci95_two_way'][0]:.6f}, {fidelity['ci95_two_way'][1]:.6f}] | "
            f"{oracle['mean']:.6f} [{oracle['ci95_two_way'][0]:.6f}, {oracle['ci95_two_way'][1]:.6f}] |"
        )
    lines.extend([
        "",
        "The oracle template diagnostic uses the hidden target only after the decision and is not a deployable policy baseline.",
        "Full policy summaries, including q05, CVaR, switch rates, and every interval, are in summary.json.",
        "",
    ])
    return "\n".join(lines)


def _write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--replication", type=int, required=True, choices=range(4))
    parser.add_argument("--workers", type=int, default=6, choices=range(1, 7))
    parser.add_argument("--limit", type=int, default=0, help="Run evenly spaced pilot jobs; never use as final evidence.")
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output exists; R3 never overwrites a run")
    args.output.mkdir(parents=True)
    started = time.perf_counter()
    try:
        import scipy

        dataset = make_dataset(args.replication)
        thresholds = calibrate(dataset)
        jobs = make_jobs()
        pilot = bool(args.limit)
        if pilot:
            jobs = [jobs[index] for index in np.linspace(0, len(jobs) - 1, min(args.limit, len(jobs)), dtype=int)]
        manifest = {
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "python": sys.version,
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "workers": args.workers,
            "pilot": pilot,
            "replication": args.replication,
            "jobs": len(jobs),
            "target_states_per_job": 64,
            "policies": POLICIES,
            "protocol_sha256": sha256(PROTOCOL_PATH),
            "source_sha256": sha256(Path(__file__)),
            "limits": "Corrected held-out residual gate; finite-copy template-switch safety only.",
        }
        _write_json(args.output / "manifest.json", manifest)
        _write_json(args.output / "dataset.json", dataset)
        _write_json(args.output / "thresholds.json", thresholds)
        results = []
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            futures = [executor.submit(evaluate_job, job, dataset, thresholds) for job in jobs]
            for future in as_completed(futures):
                results.append(future.result())
        results.sort(key=lambda item: (
            item["code"], item["copies"], item["physical_noise"],
            item["readout_flip"], item["measurement_seed"],
        ))
        summary = summarize(results, pilot)
        _write_json(args.output / "results.json", results)
        _write_json(args.output / "summary.json", summary)
        (args.output / "REPORT.md").write_text(
            report_markdown(summary, thresholds, args.replication, pilot),
            encoding="utf-8",
        )
        _write_json(args.output / "DONE.json", {
            "state": "success",
            "seconds": time.perf_counter() - started,
        })
    except Exception as error:
        _write_json(args.output / "FAILED.json", {
            "state": "failed",
            "error": repr(error),
            "traceback": traceback.format_exc(),
        })
        raise


if __name__ == "__main__":
    main()
