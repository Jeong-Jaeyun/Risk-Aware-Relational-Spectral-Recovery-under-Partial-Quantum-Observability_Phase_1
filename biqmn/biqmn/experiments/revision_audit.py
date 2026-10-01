"""Read-only scientific audit of the submitted grids; outputs go to a new directory.

No simulation parameters or production recovery routines are changed. Bootstrap
replicates resample whole seed blocks, pairing all policies and retaining the
fixed evaluation grid. Intervals are descriptive: there are only ten seed blocks.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import sys
import time

import numpy as np

from .common import REPO_ROOT, RESULT_ROOT

SOURCES = {
    "Clean": "hybrid_c123_regime_map_c3r_260427_seed10",
    "Partial": "partial_syndrome_c3r_260427_seed10",
    "Noisy-only": "noisy_syndrome_c3r_260427_seed10",
    "Partial-plus-noisy": "partial_noisy_syndrome_c3r_260427_seed10",
    "Ambiguity-plus-measurement": "ambiguity_measurement_c3r_260427_seed10",
}


def write_json(path, payload):
    path = Path(path)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, allow_nan=False), encoding="utf-8")
    temporary.replace(path)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def policy_masks(rows):
    c2 = np.array([r["candidate_C2"] == "B" for r in rows])
    structural = np.array([
        r["c3r_gate_score_margin"] and r["c3r_gate_leave_A"] and r["c3r_gate_B_safe"]
        for r in rows
    ], dtype=bool)
    uncertainty = np.array([r["c3r_gate_uncertainty"] for r in rows], dtype=bool)
    return {
        "C2": c2,
        "score_admissibility_only": c2 & structural,
        "uncertainty_only": c2 & uncertainty,
        "C3R_replayed": c2 & structural & uncertainty,
    }


def lower_tail_mean_exact(values, fraction=0.05):
    """Mean of the lowest fraction of empirical mass, splitting boundary ties."""
    arr = np.sort(np.asarray(values, dtype=float))
    mass = len(arr) * fraction
    whole = int(np.floor(mass))
    remainder = mass - whole
    total = arr[:whole].sum()
    if remainder:
        total += remainder * arr[whole]
    return float(total / mass)


def metric_vector(gain, false_safe, oracle):
    q05 = float(np.quantile(gain, 0.05))
    return np.array([
        np.mean(gain), np.mean(false_safe), q05,
        np.mean(gain[gain <= q05 + 1e-12]),
        lower_tail_mean_exact(gain), np.mean(oracle - gain),
    ], dtype=float)


METRICS = ("mean_gain", "false_safe_rate", "q05_gain",
           "lower_tail_mean_paper", "cvar05_exact_mass", "mean_oracle_regret")


def paired_seed_bootstrap(gains, flags, oracle, seeds, *, draws, rng_seed):
    seeds = np.asarray(seeds)
    unique = np.unique(seeds)
    blocks = [np.flatnonzero(seeds == s) for s in unique]
    modes = list(gains)
    point = np.stack([metric_vector(gains[m], flags[m], oracle) for m in modes])
    replicates = np.empty((draws, len(modes), len(METRICS)))
    rng = np.random.default_rng(rng_seed)
    for b in range(draws):
        idx = np.concatenate([blocks[i] for i in rng.integers(len(blocks), size=len(blocks))])
        for j, mode in enumerate(modes):
            replicates[b, j] = metric_vector(gains[mode][idx], flags[mode][idx], oracle[idx])
    def interval(values, estimate):
        lo, hi = np.quantile(values, [0.025, 0.975])
        return {"estimate": float(estimate), "ci95": [float(lo), float(hi)]}
    return {
        "method": "paired whole-seed cluster percentile bootstrap; fixed grid",
        "seed_blocks": [int(s) for s in unique], "draws": draws, "rng_seed": rng_seed,
        "policies": {
            m: {k: interval(replicates[:, j, i], point[j, i]) for i, k in enumerate(METRICS)}
            for j, m in enumerate(modes)
        },
        "differences_vs_C2": {
            m: {k: interval(replicates[:, j, i] - replicates[:, 0, i], point[j, i] - point[0, i])
                for i, k in enumerate(METRICS)} for j, m in enumerate(modes) if j
        },
        "seed_level": {
            str(int(s)): {
                m: dict(zip(METRICS, metric_vector(gains[m][idx], flags[m][idx], oracle[idx]).tolist()))
                for m in modes
            } for s, idx in zip(unique, blocks)
        },
    }


def audit_rows(rows, *, draws=5000, rng_seed=20260927):
    masks = policy_masks(rows)
    gain_a = np.array([r["fid_gain_A"] for r in rows])
    gain_b = np.array([r["fid_gain_B"] for r in rows])
    flags_a = np.array([r["false_safe_fidelity_flag_A"] for r in rows], dtype=bool)
    flags_b = np.array([r["false_safe_fidelity_flag_B"] for r in rows], dtype=bool)
    gains = {m: np.where(mask, gain_b, gain_a) for m, mask in masks.items()}
    flags = {m: np.where(mask, flags_b, flags_a) for m, mask in masks.items()}
    for label, mode in (("C2", "C2"), ("C3R", "C3R_replayed")):
        np.testing.assert_array_equal(masks[mode], [r[f"candidate_{label}"] == "B" for r in rows])
        np.testing.assert_allclose(gains[mode], [r[f"fid_gain_{label}"] for r in rows], atol=1e-12, rtol=0)
        np.testing.assert_array_equal(flags[mode], [r[f"false_safe_fidelity_flag_{label}"] for r in rows])
    blocked = masks["C2"] & ~masks["C3R_replayed"]
    effect = (gain_a - gain_b)[blocked]
    positive = np.sort(effect[effect > 0])[::-1]
    negative = -effect[effect < 0]
    n = len(positive)
    top_n = max(1, int(np.ceil(0.1 * n))) if n else 0
    oracle = np.maximum(gain_a, gain_b)
    # Bootstrap only distinct policies, retaining exact identities in the report.
    unique_gains = {"C2": gains["C2"], "C3R": gains["C3R_replayed"]}
    unique_flags = {"C2": flags["C2"], "C3R": flags["C3R_replayed"]}
    for mode in ("score_admissibility_only", "uncertainty_only"):
        if not any(np.array_equal(masks[mode], masks[other]) for other in ("C2", "C3R_replayed")):
            unique_gains[mode] = gains[mode]
            unique_flags[mode] = flags[mode]
    return {
        "rows": len(rows), "seed_counts": dict(Counter(str(r["seed"]) for r in rows)),
        "B_admissible_count": sum(bool(r["admissible_B"]) for r in rows),
        "B_labels": dict(Counter(r["candidate_B"] for r in rows)),
        "C2_B_count": int(masks["C2"].sum()), "C3R_block_count": int(blocked.sum()),
        "gate_failures_given_C2_B": {
            key: sum(r["candidate_C2"] == "B" and not r[key] for r in rows)
            for key in ("c3r_gate_score_margin", "c3r_gate_leave_A", "c3r_gate_B_safe", "c3r_gate_uncertainty")
        },
        "ablation": {
            mode: {
                "blocks_of_C2_B": int((masks["C2"] & ~mask).sum()),
                "decision_mismatches_vs_C2": int((mask != masks["C2"]).sum()),
                "decision_mismatches_vs_C3R": int((mask != masks["C3R_replayed"]).sum()),
                "metrics": dict(zip(METRICS, metric_vector(gains[mode], flags[mode], oracle).tolist())),
            } for mode, mask in masks.items()
        },
        "blocked_effect_distribution": {
            "definition": "fid_gain_A - fid_gain_B on C2=B, C3R=A rows",
            "positive_count": int((effect > 0).sum()), "negative_count": int((effect < 0).sum()),
            "neutral_count": int((effect == 0).sum()),
            "quantiles": dict(zip(["min", "q05", "q25", "median", "q75", "q95", "max"],
                                  np.quantile(effect, [0, .05, .25, .5, .75, .95, 1]).tolist())) if len(effect) else {},
            "prevented_loss_sum": float(positive.sum()), "missed_gain_sum": float(negative.sum()),
            "net_sum": float(effect.sum()),
            "top_10pct_positive_rows_share_of_prevented_loss": float(positive[:top_n].sum()/positive.sum()) if n else None,
        },
        "bootstrap": paired_seed_bootstrap(unique_gains, unique_flags, oracle,
            [r["seed"] for r in rows], draws=draws, rng_seed=rng_seed),
    }


def structural_audit():
    from .common import build_pipeline, build_reference_bank, load_config
    from ..core.clock import clock_overlap
    from ..core.recovery import recover_via_reference_projection
    from ..core.trajectory import trajectory_distance
    results = {}
    for code in ("bitflip", "phaseflip"):
        cfg = load_config(state_config=f"states/repetition_{code}.yaml",
            experiment_config="experiment/hybrid_c123_regime_map.yaml",
            overrides={"simulation": {"backend": "linear_algebra"}})
        clean = build_pipeline(cfg)
        refs = build_reference_bank(cfg)
        traj = clean["trajectory"]
        ref_trajs = [r["trajectory"] for r in refs]
        overlap = [[abs(clock_overlap(clean["Hc"], a, b, clean["psi0_clock"]))
                    for b in clean["tau_grid"]] for a in clean["tau_grid"]]
        pairwise = [[trajectory_distance(a, b) for b in ref_trajs] for a in ref_trajs]
        density_distance = [[float(np.linalg.norm(a.densities[0]-b.densities[0])) for b in ref_trajs] for a in ref_trajs]
        raw = recover_via_reference_projection(traj, ref_trajs, clean["Hc"], clean["psi0_clock"],
            weights=cfg["recovery"]["weights"], ref_bank=ref_trajs)
        results[code] = {
            "clock_initial_state": cfg["clock"]["initial_state"],
            "clock_overlap_min": float(np.min(overlap)), "clock_overlap_max": float(np.max(overlap)),
            "max_density_change_across_clock": max(float(np.linalg.norm(r-traj.densities[0])) for r in traj.densities),
            "max_spectrum_change_across_clock": max(float(np.linalg.norm(s-traj.spectra[0])) for s in traj.spectra),
            "constraint_residual": clean["meta"]["constraint_residual"],
            "nullspace_dimension": clean["meta"]["nullspace_dim"],
            "reference_labels": [r["label"] for r in refs], "reference_spectral_distances": pairwise,
            "reference_density_frobenius_distances": density_distance,
            "stage2_apply_rule": cfg["recovery"]["stage2"]["apply_rule"],
            "objective_weights": cfg["recovery"]["weights"],
            "clean_projection_selected_label": refs[raw["best_index"]]["label"],
            "clean_projection_objectives": [s["objective"] for s in raw["scored"]],
        }
    return results


def render_report(result, path):
    text = ["# Submitted-result audit", "", "Generated from immutable 260427 seed10 raw JSON files.", "",
        "Intervals: paired whole-seed percentile bootstrap, conditional on the fixed grids. Only 10 seed blocks; no claim of out-of-grid generalization or confirmatory significance.", "",
        "| Regime | Rows | C2 proposes B | C3R blocks | Score/admissibility-only blocks | B admissible |",
        "|---|---:|---:|---:|---:|---:|"]
    for name, r in result["regimes"].items():
        text.append(f"| {name} | {r['rows']} | {r['C2_B_count']} | {r['C3R_block_count']} | {r['ablation']['score_admissibility_only']['blocks_of_C2_B']} | {r['B_admissible_count']} |")
    text += ["", "## Paired C3R minus C2 differences", "", "False-safe differences below are percentage points. Positive mean/tail gain is favorable; negative false-safe and regret is favorable.", "",
        "| Regime | Metric | Estimate | 95% seed bootstrap CI |", "|---|---|---:|---|"]
    for name, r in result["regimes"].items():
        for metric, d in r["bootstrap"]["differences_vs_C2"]["C3R"].items():
            scale = 100 if metric == "false_safe_rate" else 1
            lo, hi = np.asarray(d["ci95"]) * scale
            text.append(f"| {name} | {metric} | {scale*d['estimate']:.6g} | [{lo:.6g}, {hi:.6g}] |")
    text += ["", "The original tail mean averages every observation at/below q05 (with tolerance 1e-12). With ties this may contain more than 5% of the mass. cvar05_exact_mass is reported as a sensitivity definition; the original values are preserved.", "",
        "## Structural checks", "", "See structural_checks.json for numeric evidence and source_manifest.json for hashes.", ""]
    for code, s in result["structural_checks"].items():
        text += [f"- {code}: clock overlap minimum {s['clock_overlap_min']:.16g}; maximum slice change {s['max_density_change_across_clock']:.3g}; constraint residual {s['constraint_residual']:.6g}; kernel dimension {s['nullspace_dimension']}."]
    text += ["", "With |+> and H_C=0.8 X, clock kets differ only by global phase. The projector and all normalized conditional slices are constant for any fixed joint density. The cosine-overlap formula applies to a different initial clock state.", "",
        "Encoded preparation uses c0|0>|0_L> + c1|1>|1_L>; H_S=0, so the submitted encoded state is not a zero-energy Page-Wootters state. Candidate A uses the complete syndrome recovery channel on each density; degraded observations affect the controller, not A's correction channel. These are substantive scope limitations, not just missing equations.", "",
        "The retained C2 proposal and candidate B still use relational features. Equivalence of the extra uncertainty veto does not prove that the entire pipeline is independent of those features. Candidate-generation baselines are evaluated separately."]
    path.write_text("\n".join(text) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--draws", type=int, default=5000)
    args = parser.parse_args()
    if args.draws < 2:
        parser.error("--draws must be at least 2")
    args.output.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    manifest = {"created_utc": datetime.now(timezone.utc).isoformat(), "python": sys.version,
        "executable": sys.executable, "platform": platform.platform(), "numpy": np.__version__, "sources": {}}
    source_files = list((REPO_ROOT / "biqmn").rglob("*.py")) + list((REPO_ROOT / "configs").rglob("*.yaml"))
    manifest["code_and_config_sha256"] = {str(p.relative_to(REPO_ROOT)): sha256(p) for p in source_files}
    structural = structural_audit()
    write_json(args.output / "structural_checks.json", structural)
    result = {"structural_checks": structural, "regimes": {}}
    for name, stem in SOURCES.items():
        path = RESULT_ROOT / "raw" / f"{stem}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        manifest["sources"][name] = {"path": str(path), "sha256": sha256(path),
            "grid": data["grid"], "policies": data["policies"]}
        print(f"Auditing {name}: {len(data['rows'])} rows", flush=True)
        result["regimes"][name] = audit_rows(data["rows"], draws=args.draws)
        write_json(args.output / "audit.json", result)
        effects = [{"source_row": i, "experiment_id": r["experiment_id"], "seed": r["seed"],
                    "effect": r["fid_gain_A"]-r["fid_gain_B"],
                    "raw_uncertainty": r["c3r_raw_syndrome_uncertainty"]}
                   for i, r in enumerate(data["rows"]) if r["candidate_C2"] == "B" and r["candidate_C3R"] == "A"]
        write_json(args.output / f"{name}_blocked_effects.json", effects)
    write_json(args.output / "source_manifest.json", manifest)
    render_report(result, args.output / "REPORT.md")
    write_json(args.output / "DONE.json", {"elapsed_seconds": time.perf_counter()-started})
    print(f"Completed in {time.perf_counter()-started:.1f}s: {args.output}", flush=True)


if __name__ == "__main__":
    main()
