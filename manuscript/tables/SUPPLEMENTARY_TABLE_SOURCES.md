# Supplementary Table Sources

This directory contains the CSVs used to typeset the supplementary tables.

- `paper_ready/`: compact table-level CSVs matching the manuscript tables.
- `source_tables/`: copied aggregate CSVs produced by the experiment scripts.
- `raw_csv/`: copied raw-row CSVs used for aggregate and counterfactual tables.
- `summary_md/`: copied markdown summaries produced by the experiment scripts.
- `table_manifest.csv`: table-level provenance map.

The `u_max` sensitivity table is not a direct experiment output. It is an
offline counterfactual generated from raw rows by changing only the clipped
C3R uncertainty gate while leaving candidate scores, admissibility gates, and
row-level A/B fidelity outcomes fixed.

Generated paper-ready tables:

- `clean_c2_noise_composition`: `tables\paper_ready\supp_table_clean_c2_noise_family_composition.csv`
- `clean_policy_counts`: `tables\paper_ready\supp_table_clean_policy_counts.csv`
- `intervention`: `tables\paper_ready\supp_table_intervention_quality.csv`
- `kappa`: `tables\paper_ready\supp_table_kappa_sensitivity.csv`
- `noisy_counts`: `tables\paper_ready\supp_table_noisy_syndrome_policy_counts.csv`
- `normalized`: `tables\paper_ready\supp_table_normalized_intervention_effects.csv`
- `partial_counts`: `tables\paper_ready\supp_table_partial_syndrome_policy_counts.csv`
- `partial_noisy_counts`: `tables\paper_ready\supp_table_partial_noisy_policy_counts.csv`
- `regime`: `tables\paper_ready\supp_table_regime_level_comparison.csv`
- `tail_oracle`: `tables\paper_ready\supp_table_lower_tail_oracle.csv`
- `umax`: `tables\paper_ready\supp_table_umax_sensitivity.csv`
- `uncertainty_bins`: `tables\paper_ready\supp_table_uncertainty_bin_intervention.csv`
