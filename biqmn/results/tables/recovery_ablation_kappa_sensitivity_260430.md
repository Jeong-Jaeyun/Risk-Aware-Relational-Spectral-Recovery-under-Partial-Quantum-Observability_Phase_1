# Recovery Ablation

## Overall

| cases | stage2_applied_rate | stage2_candidate_improvement_rate | recovered_admissible_rate | mean_stage2_candidate_objective_gain_vs_stage1 | mean_stage2_clean_distance_delta_vs_stage1 | stage2_helpful_tradeoff_rate | corr_gain_vs_clean_delta | corr_gain_vs_obs_fit_delta | corr_gain_vs_ref_anchor_delta | corr_gain_vs_phi_ref_delta | corr_gain_vs_clock_delta | corr_gain_vs_smooth_delta |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 135 | 0.0000 | 0.6296 | 0.7333 | 0.0768 | 0.0563 | 0.1111 | 0.1893 | -0.5854 | 0.2117 | 0.2424 | -0.1920 | -0.1986 |

## By Noise Kind

| noise_kind | cases | stage2_applied_rate | stage2_candidate_improvement_rate | mean_stage2_candidate_objective_gain_vs_stage1 | mean_stage2_clean_distance_delta_vs_stage1 | stage2_helpful_tradeoff_rate |
| --- | --- | --- | --- | --- | --- | --- |
| bitflip | 45 | 0.0000 | 0.7778 | 0.5192 | 0.0649 | 0.1333 |
| dephasing | 45 | 0.0000 | 0.6889 | 0.1784 | 0.0497 | 0.1333 |
| phaseflip | 45 | 0.0000 | 0.4222 | -0.4671 | 0.0542 | 0.0667 |

## By Admissibility Kappa

| admissibility_kappa | cases | stage2_applied_rate | stage2_candidate_improvement_rate | mean_stage2_candidate_objective_gain_vs_stage1 | stage2_helpful_tradeoff_rate |
| --- | --- | --- | --- | --- | --- |
| 1.0000 | 45 | 0.0000 | 0.5556 | -0.1100 | 0.1111 |
| 1.5000 | 45 | 0.0000 | 0.6667 | 0.1702 | 0.1111 |
| 2.0000 | 45 | 0.0000 | 0.6667 | 0.1702 | 0.1111 |

## By Bank Width

| bank_width_deg | cases | stage2_applied_rate | stage2_candidate_improvement_rate | mean_stage2_candidate_objective_gain_vs_stage1 | stage2_helpful_tradeoff_rate |
| --- | --- | --- | --- | --- | --- |
| 5.0000 | 45 | 0.0000 | 0.5556 | 0.0091 | 0.3333 |
| 10.0000 | 45 | 0.0000 | 0.7333 | 0.4137 | 0.0000 |
| 20.0000 | 45 | 0.0000 | 0.6000 | -0.1922 | 0.0000 |

## Taxonomy By Noise Kind

| noise_kind | stage2_candidate_taxonomy | cases | rate |
| --- | --- | --- | --- |
| bitflip | objective_improves_clean_improves | 6 | 0.1333 |
| bitflip | objective_improves_clean_worsens | 29 | 0.6444 |
| bitflip | objective_worsens_clean_improves | 9 | 0.2000 |
| bitflip | objective_worsens_clean_worsens | 1 | 0.0222 |
| dephasing | objective_improves_clean_improves | 6 | 0.1333 |
| dephasing | objective_improves_clean_worsens | 25 | 0.5556 |
| dephasing | objective_worsens_clean_improves | 3 | 0.0667 |
| dephasing | objective_worsens_clean_worsens | 11 | 0.2444 |
| phaseflip | objective_improves_clean_improves | 3 | 0.0667 |
| phaseflip | objective_improves_clean_worsens | 16 | 0.3556 |
| phaseflip | objective_worsens_clean_worsens | 26 | 0.5778 |

## Dominant Weighted Term By Noise Kind

| noise_kind | stage2_candidate_dominant_weighted_term | cases | rate |
| --- | --- | --- | --- |
| bitflip | obs_fit | 15 | 0.3333 |
| bitflip | smooth | 30 | 0.6667 |
| dephasing | obs_fit | 9 | 0.2000 |
| dephasing | smooth | 36 | 0.8000 |
| phaseflip | obs_fit | 3 | 0.0667 |
| phaseflip | smooth | 42 | 0.9333 |

## Stage-2 Location By Noise Kind

| noise_kind | stage2_candidate_location | cases | rate |
| --- | --- | --- | --- |
| bitflip | interior | 45 | 1.0000 |
| dephasing | interior | 45 | 1.0000 |
| phaseflip | interior | 45 | 1.0000 |

## By Stage-2 Location

| stage2_candidate_location | cases | stage2_applied_rate | stage2_candidate_improvement_rate | mean_stage2_candidate_objective_gain_vs_stage1 | mean_stage2_clean_distance_delta_vs_stage1 | stage2_helpful_tradeoff_rate |
| --- | --- | --- | --- | --- | --- | --- |
| interior | 135 | 0.0000 | 0.6296 | 0.0768 | 0.0563 | 0.1111 |
