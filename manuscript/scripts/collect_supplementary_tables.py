"""Collect paper-ready supplementary tables and their provenance.

The supplementary manuscript currently typesets several compact tables by hand.
This script recreates those table-level CSVs from the latest C3R result outputs
and copies the relevant source files under manuscript/tables.
"""

from __future__ import annotations

import csv
import shutil
import sys
from collections import Counter
from pathlib import Path
from typing import Any


MANUSCRIPT_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = MANUSCRIPT_DIR.parent
BIQMN_DIR = PROJECT_DIR / "biqmn"
RESULT_TABLES_DIR = BIQMN_DIR / "results" / "tables"
RESULT_RAW_DIR = BIQMN_DIR / "results" / "raw"

sys.path.insert(0, str(BIQMN_DIR))

from biqmn.experiments.run_hybrid_c123_baseline import (  # noqa: E402
    _aggregate_rows,
    enrich_c3r_row,
)


OUT_DIR = MANUSCRIPT_DIR / "tables"
PAPER_READY_DIR = OUT_DIR / "paper_ready"
SOURCE_TABLES_DIR = OUT_DIR / "source_tables"
RAW_CSV_DIR = OUT_DIR / "raw_csv"
SUMMARY_MD_DIR = OUT_DIR / "summary_md"


REGIMES = [
    ("Clean", "hybrid_c123_regime_map_c3r_260427_seed10"),
    ("Partial", "partial_syndrome_c3r_260427_seed10"),
    ("Noisy-only", "noisy_syndrome_c3r_260427_seed10"),
    ("Partial+noisy", "partial_noisy_syndrome_c3r_260427_seed10"),
    ("Ambig.+meas.", "ambiguity_measurement_c3r_260427_seed10"),
]

UMAX_REGIMES = [
    ("Partial", "partial_syndrome_c3r_260427_seed10"),
    ("Partial+noisy", "partial_noisy_syndrome_c3r_260427_seed10"),
    ("Ambig.+meas.", "ambiguity_measurement_c3r_260427_seed10"),
    ("Noisy-only", "noisy_syndrome_c3r_260427_seed10"),
]


SOURCE_TABLE_FILES = [
    "hybrid_c123_regime_map_c3r_260427_seed10_preferred_policy_summary.csv",
    "hybrid_c123_regime_map_c3r_260427_seed10_by_regime_cell.csv",
    "partial_syndrome_c3r_260427_seed10_preferred_policy_counts_by_ratio.csv",
    "noisy_syndrome_c3r_260427_seed10_preferred_policy_counts_by_noise.csv",
    "partial_noisy_syndrome_c3r_260427_seed10_preferred_policy_counts_by_combo.csv",
    "recovery_ablation_kappa_sensitivity_260430_by_admissibility_kappa.csv",
    "partial_syndrome_c3r_260427_seed10_c3r_by_uncertainty_bin.csv",
    "partial_noisy_syndrome_c3r_260427_seed10_c3r_by_uncertainty_bin.csv",
    "ambiguity_measurement_c3r_260427_seed10_c3r_by_uncertainty_bin.csv",
]


def parse_csv_value(value: str) -> Any:
    if value == "True":
        return True
    if value == "False":
        return False
    return value


def read_csv(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8-sig") as fh:
        return [
            {key: parse_csv_value(value) for key, value in row.items()}
            for row in csv.DictReader(fh)
        ]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def copy_if_exists(path: Path, dest_dir: Path) -> str:
    if not path.exists():
        return ""
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / path.name
    shutil.copy2(path, dest)
    return str(dest.relative_to(MANUSCRIPT_DIR))


def raw_csv_path(stem: str) -> Path:
    return RESULT_TABLES_DIR / f"{stem}_raw.csv"


def raw_json_path(stem: str) -> Path:
    return RESULT_RAW_DIR / f"{stem}.json"


def summary_md_path(stem: str) -> Path:
    return RESULT_TABLES_DIR / f"{stem}.md"


def load_raw(stem: str) -> list[dict[str, Any]]:
    return read_csv(raw_csv_path(stem))


def aggregate(stem: str) -> dict[str, Any]:
    return _aggregate_rows(load_raw(stem))


def source_tables() -> None:
    for filename in SOURCE_TABLE_FILES:
        copy_if_exists(RESULT_TABLES_DIR / filename, SOURCE_TABLES_DIR)
    for _regime, stem in REGIMES:
        copy_if_exists(raw_csv_path(stem), RAW_CSV_DIR)
        copy_if_exists(summary_md_path(stem), SUMMARY_MD_DIR)


def clean_policy_counts() -> str:
    rows = read_csv(RESULT_TABLES_DIR / "hybrid_c123_regime_map_c3r_260427_seed10_preferred_policy_summary.csv")
    counts = {str(row["preferred_policy"]): int(float(row["cases"])) for row in rows}
    total = sum(counts.values())
    output = []
    interpretations = {
        "C1": "Default conservative hybrid region.",
        "C2": "Structured correction region; all cells are phase-flip code rows.",
        "C3": "No independent strict-admissibility zone.",
        "C3R": "No clean-regime veto trigger at the default gate.",
    }
    for policy in ("C1", "C2", "C3", "C3R"):
        cells = counts.get(policy, 0)
        output.append(
            {
                "policy": policy,
                "cells": cells,
                "share": cells / total if total else 0.0,
                "interpretation": interpretations[policy],
            }
        )
    path = PAPER_READY_DIR / "supp_table_clean_policy_counts.csv"
    write_csv(path, output)
    return str(path.relative_to(MANUSCRIPT_DIR))


def clean_c2_noise_composition() -> str:
    rows = read_csv(RESULT_TABLES_DIR / "hybrid_c123_regime_map_c3r_260427_seed10_by_regime_cell.csv")
    counts: Counter[str] = Counter()
    for row in rows:
        if str(row.get("preferred_policy")) == "C2":
            counts[str(row["noise_family"])] += 1
    labels = {
        "bitflip": "Bit flip",
        "bit_flip": "Bit flip",
        "dephasing": "Dephasing",
        "depolarizing": "Depolarizing",
        "mixed_pauli": "Mixed Pauli",
        "phaseflip": "Phase flip",
        "phase_flip": "Phase flip",
    }
    output = [
        {
            "noise_family": labels.get(key, key),
            "c2_preferred_cells": counts[key],
        }
        for key in sorted(counts)
    ]
    path = PAPER_READY_DIR / "supp_table_clean_c2_noise_family_composition.csv"
    write_csv(path, output)
    return str(path.relative_to(MANUSCRIPT_DIR))


def direct_policy_count_table(source_name: str, output_name: str) -> str:
    rows = read_csv(RESULT_TABLES_DIR / source_name)
    path = PAPER_READY_DIR / output_name
    write_csv(path, rows)
    return str(path.relative_to(MANUSCRIPT_DIR))


def project_c3r_row(row: dict[str, Any], uncertainty_max: float) -> dict[str, Any]:
    item = dict(row)
    gate_c2_switch = bool(item["c3r_gate_c2_switch"])
    gate_score_margin = bool(item["c3r_gate_score_margin"])
    gate_leave_A = bool(item["c3r_gate_leave_A"])
    gate_b_safe = bool(item["c3r_gate_B_safe"])
    gate_uncertainty = float(item["c3r_syndrome_uncertainty"]) <= float(uncertainty_max)
    allow_b = bool(
        gate_c2_switch
        and gate_score_margin
        and gate_leave_A
        and gate_b_safe
        and gate_uncertainty
    )
    chosen = "B" if allow_b else "A"

    if allow_b:
        reason = "c3r_all_gates_pass"
    elif not gate_c2_switch:
        reason = "c3r_c2_preserves_A"
    elif not gate_score_margin:
        reason = "c3r_blocks_low_score_margin"
    elif not gate_leave_A:
        reason = "c3r_blocks_insufficient_A_risk"
    elif not gate_b_safe:
        reason = "c3r_blocks_unsafe_B"
    elif not gate_uncertainty:
        reason = "c3r_blocks_high_syndrome_uncertainty"
    else:
        reason = "c3r_blocks_unknown"

    for field in (
        "admissible",
        "objective",
        "traj_distance",
        "traj_distance_to_clean",
        "fidelity_after",
        "fid_gain",
        "logical_success",
        "false_safe_flag",
        "false_safe_fidelity_flag",
        "nonworsen",
        "failure_boundary_flag",
        "observed_failure_boundary_flag",
        "true_failure_boundary_flag",
    ):
        item[f"{field}_C3R"] = item[f"{field}_{chosen}"]

    item["candidate_C3R"] = chosen
    item["decision_reason_C3R"] = reason
    item["decision_disagreement_rate_C3RA_flag"] = chosen != "A"
    item["decision_disagreement_C3R_vs_C2_flag"] = chosen != str(item["candidate_C2"])
    item["c3r_gate_uncertainty"] = gate_uncertainty
    item["c3r_allow_B"] = allow_b
    item["violation_C3R"] = item["c3r_violation_B"] if chosen == "B" else item["c3r_violation_A"]
    item["fidelity_margin"] = 0.01
    return enrich_c3r_row(item)


def umax_sensitivity() -> str:
    output = []
    for regime, stem in UMAX_REGIMES:
        rows = load_raw(stem)
        for umax in (0.75, 0.99, 1.00):
            projected = [project_c3r_row(row, umax) for row in rows]
            agg = _aggregate_rows(projected)
            blocked = int(agg["c3r_block_count"])
            output.append(
                {
                    "regime": regime,
                    "u_max": umax,
                    "mean_gain_C3R": agg["fid_gain_C3R_mean"],
                    "false_safe_fidelity_rate_C3R": agg["false_safe_fidelity_rate_C3R"],
                    "blocked": blocked,
                    "harmful_block_precision": "" if blocked == 0 else agg["c3r_harmful_block_precision"],
                    "beneficial_switch_block_rate": "" if blocked == 0 else agg["c3r_beneficial_switch_block_rate"],
                    "net_intervention_gain": agg["c3r_net_intervention_gain"],
                    "net_per_block": "" if blocked == 0 else agg["c3r_net_intervention_gain"] / blocked,
                }
            )
    path = PAPER_READY_DIR / "supp_table_umax_sensitivity.csv"
    write_csv(path, output)
    return str(path.relative_to(MANUSCRIPT_DIR))


def kappa_sensitivity() -> str:
    rows = read_csv(RESULT_TABLES_DIR / "recovery_ablation_kappa_sensitivity_260430_by_admissibility_kappa.csv")
    output = [
        {
            "kappa": row["admissibility_kappa"],
            "cases": row["cases"],
            "recovered_admissible_rate": row["recovered_admissible_rate"],
            "stage2_candidate_improvement_rate": row["stage2_candidate_improvement_rate"],
            "mean_stage2_candidate_objective_gain_vs_stage1": row[
                "mean_stage2_candidate_objective_gain_vs_stage1"
            ],
            "stage2_helpful_tradeoff_rate": row["stage2_helpful_tradeoff_rate"],
        }
        for row in rows
    ]
    path = PAPER_READY_DIR / "supp_table_kappa_sensitivity.csv"
    write_csv(path, output)
    return str(path.relative_to(MANUSCRIPT_DIR))


def regime_level_comparison() -> str:
    output = []
    for regime, stem in REGIMES:
        agg = aggregate(stem)
        output.append(
            {
                "regime": regime,
                "n": agg["cases"],
                "mean_gain_C2": agg["fid_gain_C2_mean"],
                "mean_gain_C3R": agg["fid_gain_C3R_mean"],
                "logical_success_C2": agg["logical_success_rate_C2"],
                "logical_success_C3R": agg["logical_success_rate_C3R"],
                "nonworsen_C2": agg["nonworsen_rate_C2"],
                "nonworsen_C3R": agg["nonworsen_rate_C3R"],
                "false_safe_fidelity_C2": agg["false_safe_fidelity_rate_C2"],
                "false_safe_fidelity_C3R": agg["false_safe_fidelity_rate_C3R"],
                "true_failure_boundary_C2": agg["true_failure_boundary_rate_C2"],
                "true_failure_boundary_C3R": agg["true_failure_boundary_rate_C3R"],
            }
        )
    path = PAPER_READY_DIR / "supp_table_regime_level_comparison.csv"
    write_csv(path, output)
    return str(path.relative_to(MANUSCRIPT_DIR))


def lower_tail_oracle() -> str:
    output = []
    for regime, stem in REGIMES:
        agg = aggregate(stem)
        output.append(
            {
                "regime": regime,
                "q05_C2": agg["fid_gain_q05_C2"],
                "q05_C3R": agg["fid_gain_q05_C3R"],
                "cvar05_C2": agg["fid_gain_cvar05_C2"],
                "cvar05_C3R": agg["fid_gain_cvar05_C3R"],
                "oracle_regret_mean_C2": agg["oracle_regret_mean_C2"],
                "oracle_regret_mean_C3R": agg["oracle_regret_mean_C3R"],
                "raw_uncertainty_mean": agg["c3r_raw_syndrome_uncertainty_mean"],
            }
        )
    path = PAPER_READY_DIR / "supp_table_lower_tail_oracle.csv"
    write_csv(path, output)
    return str(path.relative_to(MANUSCRIPT_DIR))


def intervention_quality() -> str:
    output = []
    for regime, stem in REGIMES:
        agg = aggregate(stem)
        if int(agg["c3r_block_count"]) == 0:
            continue
        output.append(
            {
                "regime": regime,
                "c2_B": agg["c2_B_count"],
                "blocked": agg["c3r_block_count"],
                "block_rate_given_c2_B": agg["c3r_block_rate_given_c2_B"],
                "harmful_block_precision": agg["c3r_harmful_block_precision"],
                "harmful_switch_recall": agg["c3r_harmful_switch_recall"],
                "beneficial_switch_block_rate": agg["c3r_beneficial_switch_block_rate"],
                "net_intervention_gain": agg["c3r_net_intervention_gain"],
            }
        )
    path = PAPER_READY_DIR / "supp_table_intervention_quality.csv"
    write_csv(path, output)
    return str(path.relative_to(MANUSCRIPT_DIR))


def normalized_intervention_effects() -> str:
    output = []
    for regime, stem in REGIMES:
        agg = aggregate(stem)
        blocked = int(agg["c3r_block_count"])
        c2_b = int(agg["c2_B_count"])
        if blocked == 0:
            continue
        net = float(agg["c3r_net_intervention_gain"])
        output.append(
            {
                "regime": regime,
                "blocked": blocked,
                "prevented": agg["c3r_prevented_loss_sum"],
                "missed": agg["c3r_missed_gain_sum"],
                "net": net,
                "net_per_block": net / blocked,
                "net_per_c2_B": net / c2_b if c2_b else "",
            }
        )
    path = PAPER_READY_DIR / "supp_table_normalized_intervention_effects.csv"
    write_csv(path, output)
    return str(path.relative_to(MANUSCRIPT_DIR))


def uncertainty_subset_row(regime: str, label: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    agg = _aggregate_rows(rows)
    blocked = int(agg["c3r_block_count"])
    return {
        "regime": regime,
        "u_raw_bin": label,
        "cases": agg["cases"],
        "c2_B": agg["c2_B_count"],
        "blocked": blocked,
        "block_rate_given_c2_B": agg["c3r_block_rate_given_c2_B"],
        "harmful_block_precision": "" if blocked == 0 else agg["c3r_harmful_block_precision"],
        "net_intervention_gain": agg["c3r_net_intervention_gain"],
    }


def uncertainty_bin_intervention() -> str:
    output: list[dict[str, Any]] = []

    partial = load_raw("partial_syndrome_c3r_260427_seed10")
    output.append(
        uncertainty_subset_row(
            "Partial",
            "<1.00",
            [row for row in partial if float(row["c3r_raw_syndrome_uncertainty"]) < 1.0],
        )
    )
    output.append(
        uncertainty_subset_row(
            "Partial",
            "[1,+inf)",
            [row for row in partial if float(row["c3r_raw_syndrome_uncertainty"]) >= 1.0],
        )
    )

    partial_noisy = load_raw("partial_noisy_syndrome_c3r_260427_seed10")
    output.append(
        uncertainty_subset_row(
            "Partial+noisy",
            "[0.75,1.00)",
            [
                row
                for row in partial_noisy
                if 0.75 <= float(row["c3r_raw_syndrome_uncertainty"]) < 1.0
            ],
        )
    )
    output.append(
        uncertainty_subset_row(
            "Partial+noisy",
            "[1,+inf)",
            [row for row in partial_noisy if float(row["c3r_raw_syndrome_uncertainty"]) >= 1.0],
        )
    )

    ambiguity = load_raw("ambiguity_measurement_c3r_260427_seed10")
    output.append(
        uncertainty_subset_row(
            "Ambig.+meas.",
            "<1.00",
            [row for row in ambiguity if float(row["c3r_raw_syndrome_uncertainty"]) < 1.0],
        )
    )
    output.append(
        uncertainty_subset_row(
            "Ambig.+meas.",
            "[1,+inf)",
            [row for row in ambiguity if float(row["c3r_raw_syndrome_uncertainty"]) >= 1.0],
        )
    )

    path = PAPER_READY_DIR / "supp_table_uncertainty_bin_intervention.csv"
    write_csv(path, output)
    return str(path.relative_to(MANUSCRIPT_DIR))


def manifest(paths: dict[str, str]) -> None:
    rows = [
        {
            "table_id": "clean_policy_counts",
            "paper_ready_csv": paths["clean_policy_counts"],
            "source_table_csv": str((RESULT_TABLES_DIR / SOURCE_TABLE_FILES[0]).relative_to(PROJECT_DIR)),
            "source_raw_csv": "",
            "source_raw_json": str(raw_json_path("hybrid_c123_regime_map_c3r_260427_seed10").relative_to(PROJECT_DIR)),
            "notes": "Counts copied from the clean preferred-policy summary; C3 and C3R zero rows are explicit manuscript rows.",
        },
        {
            "table_id": "clean_c2_noise_family_composition",
            "paper_ready_csv": paths["clean_c2_noise_composition"],
            "source_table_csv": str((RESULT_TABLES_DIR / "hybrid_c123_regime_map_c3r_260427_seed10_by_regime_cell.csv").relative_to(PROJECT_DIR)),
            "source_raw_csv": "",
            "source_raw_json": str(raw_json_path("hybrid_c123_regime_map_c3r_260427_seed10").relative_to(PROJECT_DIR)),
            "notes": "Filtered rows with preferred_policy == C2 and counted noise_family.",
        },
        {
            "table_id": "partial_policy_counts",
            "paper_ready_csv": paths["partial_counts"],
            "source_table_csv": str((RESULT_TABLES_DIR / "partial_syndrome_c3r_260427_seed10_preferred_policy_counts_by_ratio.csv").relative_to(PROJECT_DIR)),
            "source_raw_csv": "",
            "source_raw_json": str(raw_json_path("partial_syndrome_c3r_260427_seed10").relative_to(PROJECT_DIR)),
            "notes": "Direct copy of preferred-policy counts by observation ratio.",
        },
        {
            "table_id": "noisy_policy_counts",
            "paper_ready_csv": paths["noisy_counts"],
            "source_table_csv": str((RESULT_TABLES_DIR / "noisy_syndrome_c3r_260427_seed10_preferred_policy_counts_by_noise.csv").relative_to(PROJECT_DIR)),
            "source_raw_csv": "",
            "source_raw_json": str(raw_json_path("noisy_syndrome_c3r_260427_seed10").relative_to(PROJECT_DIR)),
            "notes": "Direct copy of preferred-policy counts by syndrome-noise probability.",
        },
        {
            "table_id": "partial_noisy_policy_counts",
            "paper_ready_csv": paths["partial_noisy_counts"],
            "source_table_csv": str((RESULT_TABLES_DIR / "partial_noisy_syndrome_c3r_260427_seed10_preferred_policy_counts_by_combo.csv").relative_to(PROJECT_DIR)),
            "source_raw_csv": "",
            "source_raw_json": str(raw_json_path("partial_noisy_syndrome_c3r_260427_seed10").relative_to(PROJECT_DIR)),
            "notes": "Direct copy of representative preferred-policy counts by observation ratio and noise probability.",
        },
        {
            "table_id": "umax_sensitivity",
            "paper_ready_csv": paths["umax"],
            "source_table_csv": "",
            "source_raw_csv": "; ".join(str(raw_csv_path(stem).relative_to(PROJECT_DIR)) for _regime, stem in UMAX_REGIMES),
            "source_raw_json": "; ".join(str(raw_json_path(stem).relative_to(PROJECT_DIR)) for _regime, stem in UMAX_REGIMES),
            "notes": "Offline counterfactual recomputed from raw rows by changing only the C3R uncertainty gate.",
        },
        {
            "table_id": "kappa_sensitivity",
            "paper_ready_csv": paths["kappa"],
            "source_table_csv": str((RESULT_TABLES_DIR / "recovery_ablation_kappa_sensitivity_260430_by_admissibility_kappa.csv").relative_to(PROJECT_DIR)),
            "source_raw_csv": "",
            "source_raw_json": str((RESULT_RAW_DIR / "recovery_ablation_kappa_sensitivity_260430.json").relative_to(PROJECT_DIR)),
            "notes": "Direct projection of admissibility-kappa sweep summary.",
        },
        {
            "table_id": "uncertainty_bin_intervention",
            "paper_ready_csv": paths["uncertainty_bins"],
            "source_table_csv": "; ".join(
                str((RESULT_TABLES_DIR / filename).relative_to(PROJECT_DIR))
                for filename in SOURCE_TABLE_FILES[-3:]
            ),
            "source_raw_csv": "; ".join(
                str(raw_csv_path(stem).relative_to(PROJECT_DIR))
                for stem in (
                    "partial_syndrome_c3r_260427_seed10",
                    "partial_noisy_syndrome_c3r_260427_seed10",
                    "ambiguity_measurement_c3r_260427_seed10",
                )
            ),
            "source_raw_json": "",
            "notes": "Manuscript bins are compact aggregations of the default raw-row uncertainty bins.",
        },
        {
            "table_id": "regime_level_comparison",
            "paper_ready_csv": paths["regime"],
            "source_table_csv": "",
            "source_raw_csv": "; ".join(str(raw_csv_path(stem).relative_to(PROJECT_DIR)) for _regime, stem in REGIMES),
            "source_raw_json": "; ".join(str(raw_json_path(stem).relative_to(PROJECT_DIR)) for _regime, stem in REGIMES),
            "notes": "Recomputed with the same aggregate helper used by the experiment code.",
        },
        {
            "table_id": "lower_tail_oracle",
            "paper_ready_csv": paths["tail_oracle"],
            "source_table_csv": "",
            "source_raw_csv": "; ".join(str(raw_csv_path(stem).relative_to(PROJECT_DIR)) for _regime, stem in REGIMES),
            "source_raw_json": "; ".join(str(raw_json_path(stem).relative_to(PROJECT_DIR)) for _regime, stem in REGIMES),
            "notes": "Recomputed lower-tail and oracle-regret summaries from raw rows.",
        },
        {
            "table_id": "intervention_quality",
            "paper_ready_csv": paths["intervention"],
            "source_table_csv": "",
            "source_raw_csv": "; ".join(str(raw_csv_path(stem).relative_to(PROJECT_DIR)) for _regime, stem in REGIMES),
            "source_raw_json": "; ".join(str(raw_json_path(stem).relative_to(PROJECT_DIR)) for _regime, stem in REGIMES),
            "notes": "Recomputed C3R intervention diagnostics and kept only non-zero blocking regimes.",
        },
        {
            "table_id": "normalized_intervention_effects",
            "paper_ready_csv": paths["normalized"],
            "source_table_csv": "",
            "source_raw_csv": "; ".join(str(raw_csv_path(stem).relative_to(PROJECT_DIR)) for _regime, stem in REGIMES),
            "source_raw_json": "; ".join(str(raw_json_path(stem).relative_to(PROJECT_DIR)) for _regime, stem in REGIMES),
            "notes": "Derived from aggregate prevented/missed/net intervention sums.",
        },
    ]
    write_csv(OUT_DIR / "table_manifest.csv", rows)


def readme(paths: dict[str, str]) -> None:
    lines = [
        "# Supplementary Table Sources",
        "",
        "This directory contains the CSVs used to typeset the supplementary tables.",
        "",
        "- `paper_ready/`: compact table-level CSVs matching the manuscript tables.",
        "- `source_tables/`: copied aggregate CSVs produced by the experiment scripts.",
        "- `raw_csv/`: copied raw-row CSVs used for aggregate and counterfactual tables.",
        "- `summary_md/`: copied markdown summaries produced by the experiment scripts.",
        "- `table_manifest.csv`: table-level provenance map.",
        "",
        "The `u_max` sensitivity table is not a direct experiment output. It is an",
        "offline counterfactual generated from raw rows by changing only the clipped",
        "C3R uncertainty gate while leaving candidate scores, admissibility gates, and",
        "row-level A/B fidelity outcomes fixed.",
        "",
        "Generated paper-ready tables:",
        "",
    ]
    for key, relpath in sorted(paths.items()):
        lines.append(f"- `{key}`: `{relpath}`")
    lines.append("")
    (OUT_DIR / "SUPPLEMENTARY_TABLE_SOURCES.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    source_tables()
    paths = {
        "clean_policy_counts": clean_policy_counts(),
        "clean_c2_noise_composition": clean_c2_noise_composition(),
        "partial_counts": direct_policy_count_table(
            "partial_syndrome_c3r_260427_seed10_preferred_policy_counts_by_ratio.csv",
            "supp_table_partial_syndrome_policy_counts.csv",
        ),
        "noisy_counts": direct_policy_count_table(
            "noisy_syndrome_c3r_260427_seed10_preferred_policy_counts_by_noise.csv",
            "supp_table_noisy_syndrome_policy_counts.csv",
        ),
        "partial_noisy_counts": direct_policy_count_table(
            "partial_noisy_syndrome_c3r_260427_seed10_preferred_policy_counts_by_combo.csv",
            "supp_table_partial_noisy_policy_counts.csv",
        ),
        "umax": umax_sensitivity(),
        "kappa": kappa_sensitivity(),
        "uncertainty_bins": uncertainty_bin_intervention(),
        "regime": regime_level_comparison(),
        "tail_oracle": lower_tail_oracle(),
        "intervention": intervention_quality(),
        "normalized": normalized_intervention_effects(),
    }
    manifest(paths)
    readme(paths)
    print(f"Wrote supplementary table package to {OUT_DIR}")


if __name__ == "__main__":
    main()
