# Partial Syndrome Baseline

## Overall

| cases | backend | fid_gain_C1_mean | fid_gain_C2_mean | fid_gain_C3_mean | fid_gain_C3R_mean | logical_success_rate_C2 | logical_success_rate_C3R | nonworsen_rate_C2 | nonworsen_rate_C3R | false_safe_rate_C1 | false_safe_rate_C2 | false_safe_rate_C3 | false_safe_rate_C3R | false_safe_fidelity_rate_C1 | false_safe_fidelity_rate_C2 | false_safe_fidelity_rate_C3 | false_safe_fidelity_rate_C3R | fid_gain_q05_C2 | fid_gain_q05_C3R | fid_gain_cvar05_C2 | fid_gain_cvar05_C3R | chosen_B_rate_C2 | chosen_B_rate_C3R |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2880 | qiskit_aer | 0.1164 | 0.1169 | 0.1169 | 0.1189 | 0.4552 | 0.5976 | 0.8774 | 0.9306 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0840 | 0.0694 | 0.0694 | 0.0389 | -0.0152 | -0.0006 | -0.0208 | -0.0147 | 0.3799 | 0.2146 |

## By Observation Ratio

| syndrome_observation_ratio | cases | fid_gain_C1_mean | fid_gain_C2_mean | fid_gain_C3_mean | fid_gain_C3R_mean | false_safe_rate_C1 | false_safe_rate_C2 | false_safe_rate_C3 | false_safe_rate_C3R | false_safe_fidelity_rate_C1 | false_safe_fidelity_rate_C2 | false_safe_fidelity_rate_C3 | false_safe_fidelity_rate_C3R |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.2500 | 720 | 0.1172 | 0.1172 | 0.1172 | 0.1205 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0694 | 0.0694 | 0.0694 | 0.0000 |
| 0.5000 | 720 | 0.1167 | 0.1167 | 0.1167 | 0.1213 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0722 | 0.0722 | 0.0722 | 0.0194 |
| 0.7500 | 720 | 0.1164 | 0.1164 | 0.1164 | 0.1164 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0708 | 0.0708 | 0.0708 | 0.0708 |
| 1.0000 | 720 | 0.1154 | 0.1174 | 0.1174 | 0.1174 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.1236 | 0.0653 | 0.0653 | 0.0653 |

## Preferred Policy Counts By Observation Ratio

| syndrome_observation_ratio | cases | C1_count | C2_count | C3_count | C3R_count | C1_rate | C2_rate | C3_rate | C3R_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.0000 | 72 | 37 | 35 | 0 | 0 | 0.5139 | 0.4861 | 0.0000 | 0.0000 |
| 0.7500 | 72 | 72 | 0 | 0 | 0 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| 0.5000 | 72 | 12 | 0 | 0 | 60 | 0.1667 | 0.0000 | 0.0000 | 0.8333 |
| 0.2500 | 72 | 14 | 0 | 0 | 58 | 0.1944 | 0.0000 | 0.0000 | 0.8056 |

## C3R Gate Summary

| chosen_B_rate_C2 | chosen_B_rate_C3R | decision_disagreement_rate_C3R_vs_C2 | c2_B_count | c3r_block_count | c3r_blocks_c2_switch_rate | c3r_gate_uncertainty_rate_given_c2_B | c3r_allow_B_rate_given_c2_B | c3r_prevented_harmful_switch_rate_given_block | c3r_missed_beneficial_switch_rate_given_block | c3r_raw_syndrome_uncertainty_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.3799 | 0.2146 | 0.1653 | 1094 | 476 | 0.1653 | 0.5649 | 0.5649 | 0.8697 | 0.0945 | 0.7604 |

## C3R Switch Intervention Quality

| c2_B_count | c3r_block_count | c3r_block_rate_given_c2_B | c3r_harmful_block_precision | c3r_harmful_switch_recall | c3r_beneficial_switch_block_rate | c3r_beneficial_switch_retention | c3r_prevented_loss_sum | c3r_missed_gain_sum | c3r_net_intervention_gain | c3r_intervention_gain_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1094 | 476 | 0.4351 | 0.8697 | 0.4461 | 0.3750 | 0.6250 | 12.2670 | 6.6055 | 5.6616 | 5.6616 |

## Tail Risk and Oracle Diagnostics

| fid_gain_q05_C2 | fid_gain_q05_C3R | fid_gain_cvar05_C2 | fid_gain_cvar05_C3R | observed_failure_boundary_rate_C2 | observed_failure_boundary_rate_C3R | true_failure_boundary_rate_C2 | true_failure_boundary_rate_C3R | chosen_candidate_violation_mean_C2 | chosen_candidate_violation_mean_C3R | admissible_rate_C2 | admissible_rate_C3R | oracle_regret_mean_C2 | oracle_regret_mean_C3R | oracle_regret_q95_C2 | oracle_regret_q95_C3R |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| -0.0152 | -0.0006 | -0.0208 | -0.0147 | 0.0892 | 0.0892 | 0.3611 | 0.2653 | 0.0000 | 0.0061 | 1.0000 | 0.8347 | 0.0271 | 0.0251 | 0.1498 | 0.1698 |

## C3R By Raw Uncertainty Bin

| c3r_raw_syndrome_uncertainty_bin | cases | c2_B_count | c3r_block_count | c3r_block_rate_given_c2_B | c3r_harmful_block_precision | c3r_harmful_switch_recall | c3r_beneficial_switch_block_rate | c3r_net_intervention_gain |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [0.00,0.25) | 720 | 273 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| [0.25,0.50) | 408 | 157 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| [0.50,0.75) | 318 | 121 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| [0.75,1.00) | 192 | 67 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| [1.00,+inf) | 1242 | 476 | 476 | 1.0000 | 0.8697 | 1.0000 | 1.0000 | 5.6616 |

## Figures

- `preferred_policy_counts`: `D:\Pandora_box\biqmn\results\plots\partial_syndrome_c3r_260427_seed10_preferred_policy_counts.png`
- `false_safe_fidelity_vs_ratio`: `D:\Pandora_box\biqmn\results\plots\partial_syndrome_c3r_260427_seed10_false_safe_fidelity_vs_ratio.png`
- `fid_gain_vs_ratio`: `D:\Pandora_box\biqmn\results\plots\partial_syndrome_c3r_260427_seed10_fid_gain_vs_ratio.png`
