# Coherent Veto Analysis

## Overall

| cases | score_mean | gain_B_mean | negative_gain_rate_B | false_safe_rate_A | false_safe_rate_B | decision_disagreement_rate_AB | corr_score_vs_gain_B | corr_score_vs_harmful_gap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1440 | 0.6826 | -0.0019 | 0.4319 | 0.9569 | 0.4111 | 0.5000 | 0.7386 | -0.0001 |

## By Pair

| code_type | noise_family | cases | score_mean | gain_B_mean | negative_gain_rate_B | false_safe_rate_A | decision_disagreement_rate_AB | corr_score_vs_gain_B |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bitflip | coherent_x | 720 | 0.6827 | 0.0130 | 0.0000 | 0.9556 | 0.0000 | 0.9030 |
| phaseflip | coherent_z | 720 | 0.6826 | -0.0168 | 0.8639 | 0.9583 | 1.0000 | 0.9145 |

## By Noise Strength

| noise_strength | cases | score_mean | gain_B_mean | negative_gain_rate_B | false_safe_rate_A | decision_disagreement_rate_AB |
| --- | --- | --- | --- | --- | --- | --- |
| 0.0100 | 240 | 0.0742 | -0.0150 | 0.5000 | 0.7500 | 0.5000 |
| 0.0300 | 240 | 0.2247 | -0.0141 | 0.5000 | 1.0000 | 0.5000 |
| 0.0500 | 240 | 0.3767 | -0.0124 | 0.5000 | 1.0000 | 0.5000 |
| 0.1000 | 240 | 0.7591 | -0.0048 | 0.5000 | 1.0000 | 0.5000 |
| 0.1500 | 240 | 1.1427 | 0.0084 | 0.3500 | 1.0000 | 0.5000 |
| 0.2000 | 240 | 1.5185 | 0.0264 | 0.2417 | 0.9917 | 0.5000 |

## By Noise Depth

| noise_depth | cases | score_mean | gain_B_mean | negative_gain_rate_B | false_safe_rate_A | decision_disagreement_rate_AB |
| --- | --- | --- | --- | --- | --- | --- |
| 1.0000 | 360 | 0.2835 | -0.0119 | 0.5000 | 0.8333 | 0.5000 |
| 2.0000 | 360 | 0.5477 | -0.0067 | 0.4778 | 1.0000 | 0.5000 |
| 3.0000 | 360 | 0.8156 | 0.0005 | 0.4167 | 1.0000 | 0.5000 |
| 4.0000 | 360 | 1.0837 | 0.0104 | 0.3333 | 0.9944 | 0.5000 |

## Figures

- `figure_a_score_vs_gain_B`: `D:\pandora_box\biqmn\results\plots\coherent_veto_analysis_score_vs_gain_B.png`
- `figure_d_representative_failures`: `D:\pandora_box\biqmn\results\plots\coherent_veto_analysis_representative_failures.png`

## Negative-Gain Phase-Coherent Cases

| experiment_id | noise_strength | noise_depth | seed | traj_inconsistency_score | gain_A | gain_B | gain_C | reason_C |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| phaseflip-seed11-sample024 | 0.0100 | 1.0000 | 11 | 0.0316 | 0.0000 | -0.0301 | -0.0301 | veto_nonadmissible_A |
| phaseflip-seed12-sample072 | 0.0100 | 1.0000 | 12 | 0.0316 | 0.0000 | -0.0301 | -0.0301 | veto_nonadmissible_A |
| phaseflip-seed13-sample120 | 0.0100 | 1.0000 | 13 | 0.0316 | 0.0000 | -0.0301 | -0.0301 | veto_nonadmissible_A |
| phaseflip-seed14-sample168 | 0.0100 | 1.0000 | 14 | 0.0316 | 0.0000 | -0.0301 | -0.0301 | veto_nonadmissible_A |
| phaseflip-seed16-sample264 | 0.0100 | 1.0000 | 16 | 0.0316 | 0.0000 | -0.0301 | -0.0301 | veto_nonadmissible_A |
| phaseflip-seed19-sample408 | 0.0100 | 1.0000 | 19 | 0.0316 | 0.0000 | -0.0301 | -0.0301 | veto_nonadmissible_A |
