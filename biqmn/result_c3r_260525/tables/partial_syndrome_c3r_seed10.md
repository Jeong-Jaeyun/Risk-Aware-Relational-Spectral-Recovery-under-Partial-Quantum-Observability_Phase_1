# Partial Syndrome Baseline

## Overall

| cases | backend | fid_gain_C1_mean | fid_gain_C2_mean | fid_gain_C3_mean | fid_gain_C3R_mean | false_safe_rate_C1 | false_safe_rate_C2 | false_safe_rate_C3 | false_safe_rate_C3R | false_safe_fidelity_rate_C1 | false_safe_fidelity_rate_C2 | false_safe_fidelity_rate_C3 | false_safe_fidelity_rate_C3R |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2880 | qiskit_aer | 0.1164 | 0.1169 | 0.1169 | 0.1184 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0858 | 0.0722 | 0.0722 | 0.0444 |

## By Observation Ratio

| syndrome_observation_ratio | cases | fid_gain_C1_mean | fid_gain_C2_mean | fid_gain_C3_mean | fid_gain_C3R_mean | false_safe_rate_C1 | false_safe_rate_C2 | false_safe_rate_C3 | false_safe_rate_C3R | false_safe_fidelity_rate_C1 | false_safe_fidelity_rate_C2 | false_safe_fidelity_rate_C3 | false_safe_fidelity_rate_C3R |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.2500 | 720 | 0.1169 | 0.1169 | 0.1169 | 0.1205 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0778 | 0.0778 | 0.0778 | 0.0000 |
| 0.5000 | 720 | 0.1170 | 0.1170 | 0.1170 | 0.1193 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0694 | 0.0694 | 0.0694 | 0.0361 |
| 0.7500 | 720 | 0.1166 | 0.1166 | 0.1166 | 0.1166 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0694 | 0.0694 | 0.0694 | 0.0694 |
| 1.0000 | 720 | 0.1150 | 0.1172 | 0.1172 | 0.1172 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.1264 | 0.0722 | 0.0722 | 0.0722 |

## Preferred Policy Counts By Observation Ratio

| syndrome_observation_ratio | cases | C1_count | C2_count | C3_count | C3R_count | C1_rate | C2_rate | C3_rate | C3R_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.0000 | 72 | 37 | 35 | 0 | 0 | 0.5139 | 0.4861 | 0.0000 | 0.0000 |
| 0.7500 | 72 | 72 | 0 | 0 | 0 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| 0.5000 | 72 | 18 | 0 | 0 | 54 | 0.2500 | 0.0000 | 0.0000 | 0.7500 |
| 0.2500 | 72 | 14 | 0 | 0 | 58 | 0.1944 | 0.0000 | 0.0000 | 0.8056 |

## Figures

- `preferred_policy_counts`: `D:\Pandora_box\biqmn\results\plots\partial_syndrome_c3r_seed10_preferred_policy_counts.png`
- `false_safe_fidelity_vs_ratio`: `D:\Pandora_box\biqmn\results\plots\partial_syndrome_c3r_seed10_false_safe_fidelity_vs_ratio.png`
- `fid_gain_vs_ratio`: `D:\Pandora_box\biqmn\results\plots\partial_syndrome_c3r_seed10_fid_gain_vs_ratio.png`
