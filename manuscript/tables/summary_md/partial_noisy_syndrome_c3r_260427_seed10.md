# Partial+Noisy Syndrome Regime Map

## Overall

| cases | backend | fid_gain_C1_mean | fid_gain_C2_mean | fid_gain_C3_mean | fid_gain_C3R_mean | logical_success_rate_C2 | logical_success_rate_C3R | nonworsen_rate_C2 | nonworsen_rate_C3R | false_safe_rate_C1 | false_safe_rate_C2 | false_safe_rate_C3 | false_safe_rate_C3R | false_safe_fidelity_rate_C1 | false_safe_fidelity_rate_C2 | false_safe_fidelity_rate_C3 | false_safe_fidelity_rate_C3R | fid_gain_q05_C2 | fid_gain_q05_C3R | fid_gain_cvar05_C2 | fid_gain_cvar05_C3R | chosen_B_rate_C2 | chosen_B_rate_C3R |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2160 | qiskit_aer | 0.1170 | 0.1170 | 0.1170 | 0.1212 | 0.4551 | 0.7241 | 0.8792 | 0.9755 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0685 | 0.0685 | 0.0685 | 0.0134 | -0.0104 | 0.0000 | -0.0206 | -0.0034 | 0.3801 | 0.0699 |

## By Observation Ratio And Syndrome Noise Probability

| syndrome_observation_ratio | syndrome_noise_prob | cases | fid_gain_C1_mean | fid_gain_C2_mean | fid_gain_C3_mean | fid_gain_C3R_mean | false_safe_rate_C1 | false_safe_rate_C2 | false_safe_rate_C3 | false_safe_rate_C3R | false_safe_fidelity_rate_C1 | false_safe_fidelity_rate_C2 | false_safe_fidelity_rate_C3 | false_safe_fidelity_rate_C3R |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.5000 | 0.0300 | 720 | 0.1171 | 0.1171 | 0.1171 | 0.1215 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0681 | 0.0681 | 0.0681 | 0.0167 |
| 0.5000 | 0.0500 | 720 | 0.1162 | 0.1162 | 0.1162 | 0.1207 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0639 | 0.0639 | 0.0639 | 0.0111 |
| 0.5000 | 0.1000 | 720 | 0.1176 | 0.1176 | 0.1176 | 0.1214 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0736 | 0.0736 | 0.0736 | 0.0125 |

## Preferred Policy Counts By Combined Syndrome Setting

| syndrome_observation_ratio | syndrome_noise_prob | cases | dominant_policy | C1_count | C2_count | C3_count | C3R_count | C1_rate | C2_rate | C3_rate | C3R_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.5000 | 0.0300 | 72 | C3R | 13 | 0 | 0 | 59 | 0.1806 | 0.0000 | 0.0000 | 0.8194 |
| 0.5000 | 0.0500 | 72 | C3R | 12 | 0 | 0 | 60 | 0.1667 | 0.0000 | 0.0000 | 0.8333 |
| 0.5000 | 0.1000 | 72 | C3R | 15 | 0 | 0 | 57 | 0.2083 | 0.0000 | 0.0000 | 0.7917 |

## C3R Gate Summary

| chosen_B_rate_C2 | chosen_B_rate_C3R | decision_disagreement_rate_C3R_vs_C2 | c2_B_count | c3r_block_count | c3r_blocks_c2_switch_rate | c3r_gate_uncertainty_rate_given_c2_B | c3r_allow_B_rate_given_c2_B | c3r_prevented_harmful_switch_rate_given_block | c3r_missed_beneficial_switch_rate_given_block | c3r_raw_syndrome_uncertainty_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.3801 | 0.0699 | 0.3102 | 821 | 670 | 0.3102 | 0.1839 | 0.1839 | 0.8791 | 0.0925 | 1.0989 |

## C3R Switch Intervention Quality

| c2_B_count | c3r_block_count | c3r_block_rate_given_c2_B | c3r_harmful_block_precision | c3r_harmful_switch_recall | c3r_beneficial_switch_block_rate | c3r_beneficial_switch_retention | c3r_prevented_loss_sum | c3r_missed_gain_sum | c3r_net_intervention_gain | c3r_intervention_gain_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 821 | 670 | 0.8161 | 0.8791 | 0.8475 | 0.6739 | 0.3261 | 17.4350 | 8.3139 | 9.1212 | 9.1212 |

## Tail Risk and Oracle Diagnostics

| fid_gain_q05_C2 | fid_gain_q05_C3R | fid_gain_cvar05_C2 | fid_gain_cvar05_C3R | observed_failure_boundary_rate_C2 | observed_failure_boundary_rate_C3R | true_failure_boundary_rate_C2 | true_failure_boundary_rate_C3R | chosen_candidate_violation_mean_C2 | chosen_candidate_violation_mean_C3R | admissible_rate_C2 | admissible_rate_C3R | oracle_regret_mean_C2 | oracle_regret_mean_C3R | oracle_regret_q95_C2 | oracle_regret_q95_C3R |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| -0.0104 | 0.0000 | -0.0206 | -0.0034 | 0.0000 | 0.0000 | 0.3616 | 0.1819 | 0.0000 | 0.0101 | 1.0000 | 0.6898 | 0.0271 | 0.0228 | 0.1498 | 0.1698 |

## C3R By Raw Uncertainty Bin

| c3r_raw_syndrome_uncertainty_bin | cases | c2_B_count | c3r_block_count | c3r_block_rate_given_c2_B | c3r_harmful_block_precision | c3r_harmful_switch_recall | c3r_beneficial_switch_block_rate | c3r_net_intervention_gain |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [0.75,1.00) | 516 | 180 | 29 | 0.1611 | 0.6897 | 0.1587 | 0.2105 | -0.3097 |
| [1.00,+inf) | 1644 | 641 | 641 | 1.0000 | 0.8877 | 1.0000 | 1.0000 | 9.4309 |

## Figures

- `dominant_policy_heatmap`: `D:\Pandora_box\biqmn\results\plots\partial_noisy_syndrome_c3r_260427_seed10_preferred_policy_map.png`
- `c3_rate_heatmap`: `D:\Pandora_box\biqmn\results\plots\partial_noisy_syndrome_c3r_260427_seed10_c3_rate_heatmap.png`
- `c3r_rate_heatmap`: `D:\Pandora_box\biqmn\results\plots\partial_noisy_syndrome_c3r_260427_seed10_c3r_rate_heatmap.png`
