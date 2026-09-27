# Noisy Syndrome Baseline

## Overall

| cases | backend | fid_gain_C1_mean | fid_gain_C2_mean | fid_gain_C3_mean | fid_gain_C3R_mean | logical_success_rate_C2 | logical_success_rate_C3R | nonworsen_rate_C2 | nonworsen_rate_C3R | false_safe_rate_C1 | false_safe_rate_C2 | false_safe_rate_C3 | false_safe_rate_C3R | false_safe_fidelity_rate_C1 | false_safe_fidelity_rate_C2 | false_safe_fidelity_rate_C3 | false_safe_fidelity_rate_C3R | fid_gain_q05_C2 | fid_gain_q05_C3R | fid_gain_cvar05_C2 | fid_gain_cvar05_C3R | chosen_B_rate_C2 | chosen_B_rate_C3R |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3600 | qiskit_aer | 0.1162 | 0.1169 | 0.1169 | 0.1169 | 0.4556 | 0.4556 | 0.8814 | 0.8814 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0942 | 0.0678 | 0.0678 | 0.0678 | -0.0104 | -0.0104 | -0.0207 | -0.0207 | 0.3806 | 0.3806 |

## By Syndrome Noise Probability

| syndrome_noise_prob | cases | fid_gain_C1_mean | fid_gain_C2_mean | fid_gain_C3_mean | fid_gain_C3R_mean | false_safe_rate_C1 | false_safe_rate_C2 | false_safe_rate_C3 | false_safe_rate_C3R | false_safe_fidelity_rate_C1 | false_safe_fidelity_rate_C2 | false_safe_fidelity_rate_C3 | false_safe_fidelity_rate_C3R |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 720 | 0.1149 | 0.1165 | 0.1165 | 0.1165 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.1264 | 0.0722 | 0.0722 | 0.0722 |
| 0.0100 | 720 | 0.1170 | 0.1176 | 0.1176 | 0.1176 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0958 | 0.0681 | 0.0681 | 0.0681 |
| 0.0300 | 720 | 0.1164 | 0.1169 | 0.1169 | 0.1169 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0903 | 0.0653 | 0.0653 | 0.0653 |
| 0.0500 | 720 | 0.1159 | 0.1166 | 0.1166 | 0.1166 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0889 | 0.0708 | 0.0708 | 0.0708 |
| 0.1000 | 720 | 0.1168 | 0.1171 | 0.1171 | 0.1171 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0694 | 0.0625 | 0.0625 | 0.0625 |

## Preferred Policy Counts By Syndrome Noise Probability

| syndrome_noise_prob | cases | C1_count | C2_count | C3_count | C3R_count | C1_rate | C2_rate | C3_rate | C3R_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 72 | 37 | 35 | 0 | 0 | 0.5139 | 0.4861 | 0.0000 | 0.0000 |
| 0.0100 | 72 | 49 | 23 | 0 | 0 | 0.6806 | 0.3194 | 0.0000 | 0.0000 |
| 0.0300 | 72 | 51 | 21 | 0 | 0 | 0.7083 | 0.2917 | 0.0000 | 0.0000 |
| 0.0500 | 72 | 51 | 21 | 0 | 0 | 0.7083 | 0.2917 | 0.0000 | 0.0000 |
| 0.1000 | 72 | 61 | 11 | 0 | 0 | 0.8472 | 0.1528 | 0.0000 | 0.0000 |

## C3R Gate Summary

| chosen_B_rate_C2 | chosen_B_rate_C3R | decision_disagreement_rate_C3R_vs_C2 | c2_B_count | c3r_block_count | c3r_blocks_c2_switch_rate | c3r_gate_uncertainty_rate_given_c2_B | c3r_allow_B_rate_given_c2_B | c3r_prevented_harmful_switch_rate_given_block | c3r_missed_beneficial_switch_rate_given_block | c3r_raw_syndrome_uncertainty_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.3806 | 0.3806 | 0.0000 | 1370 | 0 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0380 |

## C3R Switch Intervention Quality

| c2_B_count | c3r_block_count | c3r_block_rate_given_c2_B | c3r_harmful_block_precision | c3r_harmful_switch_recall | c3r_beneficial_switch_block_rate | c3r_beneficial_switch_retention | c3r_prevented_loss_sum | c3r_missed_gain_sum | c3r_net_intervention_gain | c3r_intervention_gain_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1370 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## Tail Risk and Oracle Diagnostics

| fid_gain_q05_C2 | fid_gain_q05_C3R | fid_gain_cvar05_C2 | fid_gain_cvar05_C3R | observed_failure_boundary_rate_C2 | observed_failure_boundary_rate_C3R | true_failure_boundary_rate_C2 | true_failure_boundary_rate_C3R | chosen_candidate_violation_mean_C2 | chosen_candidate_violation_mean_C3R | admissible_rate_C2 | admissible_rate_C3R | oracle_regret_mean_C2 | oracle_regret_mean_C3R | oracle_regret_q95_C2 | oracle_regret_q95_C3R |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| -0.0104 | -0.0104 | -0.0207 | -0.0207 | 0.1417 | 0.1417 | 0.3589 | 0.3589 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 0.0271 | 0.0271 | 0.1498 | 0.1498 |

## C3R By Raw Uncertainty Bin

| c3r_raw_syndrome_uncertainty_bin | cases | c2_B_count | c3r_block_count | c3r_block_rate_given_c2_B | c3r_harmful_block_precision | c3r_harmful_switch_recall | c3r_beneficial_switch_block_rate | c3r_net_intervention_gain |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [0.00,0.25) | 3600 | 1370 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## Figures

- `preferred_policy_counts`: `D:\Pandora_box\biqmn\results\plots\noisy_syndrome_c3r_260427_seed10_preferred_policy_counts.png`
- `false_safe_fidelity_vs_noise`: `D:\Pandora_box\biqmn\results\plots\noisy_syndrome_c3r_260427_seed10_false_safe_fidelity_vs_noise.png`
- `fid_gain_vs_noise`: `D:\Pandora_box\biqmn\results\plots\noisy_syndrome_c3r_260427_seed10_fid_gain_vs_noise.png`
