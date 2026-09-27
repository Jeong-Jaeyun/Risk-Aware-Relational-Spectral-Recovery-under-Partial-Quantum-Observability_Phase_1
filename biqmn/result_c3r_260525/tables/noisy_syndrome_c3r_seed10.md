# Noisy Syndrome Baseline

## Overall

| cases | backend | fid_gain_C1_mean | fid_gain_C2_mean | fid_gain_C3_mean | fid_gain_C3R_mean | false_safe_rate_C1 | false_safe_rate_C2 | false_safe_rate_C3 | false_safe_rate_C3R | false_safe_fidelity_rate_C1 | false_safe_fidelity_rate_C2 | false_safe_fidelity_rate_C3 | false_safe_fidelity_rate_C3R |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3600 | qiskit_aer | 0.1161 | 0.1169 | 0.1169 | 0.1169 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0992 | 0.0714 | 0.0714 | 0.0714 |

## By Syndrome Noise Probability

| syndrome_noise_prob | cases | fid_gain_C1_mean | fid_gain_C2_mean | fid_gain_C3_mean | fid_gain_C3R_mean | false_safe_rate_C1 | false_safe_rate_C2 | false_safe_rate_C3 | false_safe_rate_C3R | false_safe_fidelity_rate_C1 | false_safe_fidelity_rate_C2 | false_safe_fidelity_rate_C3 | false_safe_fidelity_rate_C3R |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 720 | 0.1147 | 0.1163 | 0.1163 | 0.1163 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.1278 | 0.0736 | 0.0736 | 0.0736 |
| 0.0100 | 720 | 0.1163 | 0.1168 | 0.1168 | 0.1168 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.1028 | 0.0722 | 0.0722 | 0.0722 |
| 0.0300 | 720 | 0.1161 | 0.1167 | 0.1167 | 0.1167 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0986 | 0.0667 | 0.0667 | 0.0667 |
| 0.0500 | 720 | 0.1164 | 0.1170 | 0.1170 | 0.1170 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0958 | 0.0792 | 0.0792 | 0.0792 |
| 0.1000 | 720 | 0.1171 | 0.1174 | 0.1174 | 0.1174 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0708 | 0.0653 | 0.0653 | 0.0653 |

## Preferred Policy Counts By Syndrome Noise Probability

| syndrome_noise_prob | cases | C1_count | C2_count | C3_count | C3R_count | C1_rate | C2_rate | C3_rate | C3R_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 72 | 39 | 33 | 0 | 0 | 0.5417 | 0.4583 | 0.0000 | 0.0000 |
| 0.0100 | 72 | 49 | 23 | 0 | 0 | 0.6806 | 0.3194 | 0.0000 | 0.0000 |
| 0.0300 | 72 | 48 | 24 | 0 | 0 | 0.6667 | 0.3333 | 0.0000 | 0.0000 |
| 0.0500 | 72 | 49 | 23 | 0 | 0 | 0.6806 | 0.3194 | 0.0000 | 0.0000 |
| 0.1000 | 72 | 62 | 10 | 0 | 0 | 0.8611 | 0.1389 | 0.0000 | 0.0000 |

## Figures

- `preferred_policy_counts`: `D:\Pandora_box\biqmn\results\plots\noisy_syndrome_c3r_seed10_preferred_policy_counts.png`
- `false_safe_fidelity_vs_noise`: `D:\Pandora_box\biqmn\results\plots\noisy_syndrome_c3r_seed10_false_safe_fidelity_vs_noise.png`
- `fid_gain_vs_noise`: `D:\Pandora_box\biqmn\results\plots\noisy_syndrome_c3r_seed10_fid_gain_vs_noise.png`
