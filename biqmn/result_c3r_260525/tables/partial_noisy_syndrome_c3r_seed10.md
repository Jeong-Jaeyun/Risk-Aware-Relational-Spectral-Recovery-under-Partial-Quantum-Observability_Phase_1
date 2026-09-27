# Partial+Noisy Syndrome Regime Map

## Overall

| cases | backend | fid_gain_C1_mean | fid_gain_C2_mean | fid_gain_C3_mean | fid_gain_C3R_mean | false_safe_rate_C1 | false_safe_rate_C2 | false_safe_rate_C3 | false_safe_rate_C3R | false_safe_fidelity_rate_C1 | false_safe_fidelity_rate_C2 | false_safe_fidelity_rate_C3 | false_safe_fidelity_rate_C3R |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2160 | qiskit_aer | 0.1168 | 0.1168 | 0.1168 | 0.1210 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0681 | 0.0681 | 0.0681 | 0.0148 |

## By Observation Ratio And Syndrome Noise Probability

| syndrome_observation_ratio | syndrome_noise_prob | cases | fid_gain_C1_mean | fid_gain_C2_mean | fid_gain_C3_mean | fid_gain_C3R_mean | false_safe_rate_C1 | false_safe_rate_C2 | false_safe_rate_C3 | false_safe_rate_C3R | false_safe_fidelity_rate_C1 | false_safe_fidelity_rate_C2 | false_safe_fidelity_rate_C3 | false_safe_fidelity_rate_C3R |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.5000 | 0.0300 | 720 | 0.1177 | 0.1177 | 0.1177 | 0.1218 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0708 | 0.0708 | 0.0708 | 0.0181 |
| 0.5000 | 0.0500 | 720 | 0.1164 | 0.1164 | 0.1164 | 0.1209 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0639 | 0.0639 | 0.0639 | 0.0153 |
| 0.5000 | 0.1000 | 720 | 0.1163 | 0.1163 | 0.1163 | 0.1205 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0694 | 0.0694 | 0.0694 | 0.0111 |

## Preferred Policy Counts By Combined Syndrome Setting

| syndrome_observation_ratio | syndrome_noise_prob | cases | dominant_policy | C1_count | C2_count | C3_count | C3R_count | C1_rate | C2_rate | C3_rate | C3R_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.5000 | 0.0300 | 72 | C3R | 13 | 0 | 0 | 59 | 0.1806 | 0.0000 | 0.0000 | 0.8194 |
| 0.5000 | 0.0500 | 72 | C3R | 11 | 0 | 0 | 61 | 0.1528 | 0.0000 | 0.0000 | 0.8472 |
| 0.5000 | 0.1000 | 72 | C3R | 13 | 0 | 0 | 59 | 0.1806 | 0.0000 | 0.0000 | 0.8194 |

## Figures

- `dominant_policy_heatmap`: `D:\Pandora_box\biqmn\results\plots\partial_noisy_syndrome_c3r_seed10_preferred_policy_map.png`
- `c3_rate_heatmap`: `D:\Pandora_box\biqmn\results\plots\partial_noisy_syndrome_c3r_seed10_c3_rate_heatmap.png`
- `c3r_rate_heatmap`: `D:\Pandora_box\biqmn\results\plots\partial_noisy_syndrome_c3r_seed10_c3r_rate_heatmap.png`
