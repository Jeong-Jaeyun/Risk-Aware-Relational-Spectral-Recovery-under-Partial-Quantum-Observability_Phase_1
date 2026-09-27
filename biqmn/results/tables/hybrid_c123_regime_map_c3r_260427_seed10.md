# Hybrid C1/C2/C3/C3R Regime Map

## Overall

| cases | backend | fid_gain_A_mean | fid_gain_B_mean | fid_gain_C1_mean | fid_gain_C2_mean | fid_gain_C3_mean | fid_gain_C3R_mean | logical_success_rate_C2 | logical_success_rate_C3R | nonworsen_rate_C2 | nonworsen_rate_C3R | false_safe_rate_A | false_safe_rate_B | false_safe_rate_C1 | false_safe_rate_C2 | false_safe_rate_C3 | false_safe_rate_C3R | false_safe_fidelity_rate_C1 | false_safe_fidelity_rate_C2 | false_safe_fidelity_rate_C3 | false_safe_fidelity_rate_C3R | fid_gain_q05_C2 | fid_gain_q05_C3R | fid_gain_cvar05_C2 | fid_gain_cvar05_C3R | chosen_B_rate_C2 | chosen_B_rate_C3R | decision_disagreement_rate_C1A | decision_disagreement_rate_C2A | decision_disagreement_rate_C3A | decision_disagreement_rate_C3RA | decision_disagreement_rate_C3R_vs_C2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2400 | qiskit_aer | 0.0744 | 0.1496 | 0.1304 | 0.1273 | 0.1273 | 0.1273 | 0.6358 | 0.6358 | 0.9554 | 0.9554 | 0.4462 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0521 | 0.0238 | 0.0238 | 0.0238 | -0.0000 | -0.0000 | -0.0033 | -0.0033 | 0.6371 | 0.6371 | 0.7983 | 0.6371 | 0.6371 | 0.6371 | 0.0000 |

## By Code And Noise Family

| code_family | noise_family | cases | fid_gain_A_mean | fid_gain_B_mean | fid_gain_C1_mean | fid_gain_C2_mean | fid_gain_C3_mean | fid_gain_C3R_mean | false_safe_rate_C1 | false_safe_rate_C2 | false_safe_rate_C3 | false_safe_rate_C3R | false_safe_fidelity_rate_C1 | false_safe_fidelity_rate_C2 | false_safe_fidelity_rate_C3 | false_safe_fidelity_rate_C3R |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bitflip | bitflip | 240 | 0.1844 | 0.1844 | 0.1844 | 0.1844 | 0.1844 | 0.1844 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| bitflip | dephasing | 240 | 0.0000 | 0.0979 | 0.0979 | 0.0979 | 0.0979 | 0.0979 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| bitflip | depolarizing | 240 | 0.0656 | 0.1904 | 0.1883 | 0.1883 | 0.1883 | 0.1883 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| bitflip | mixed_pauli | 240 | 0.0668 | 0.1885 | 0.1870 | 0.1870 | 0.1870 | 0.1870 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| bitflip | phaseflip | 240 | -0.0000 | 0.1714 | 0.1714 | 0.1714 | 0.1714 | 0.1714 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| phaseflip | bitflip | 240 | 0.0000 | 0.1412 | 0.0464 | 0.0149 | 0.0149 | 0.0149 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0833 | 0.0417 | 0.0417 | 0.0417 |
| phaseflip | dephasing | 240 | 0.1017 | 0.0716 | 0.0794 | 0.0903 | 0.0903 | 0.0903 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.1917 | 0.0833 | 0.0833 | 0.0833 |
| phaseflip | depolarizing | 240 | 0.0655 | 0.1603 | 0.0835 | 0.0784 | 0.0784 | 0.0784 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0708 | 0.0000 | 0.0000 | 0.0000 |
| phaseflip | mixed_pauli | 240 | 0.0753 | 0.1365 | 0.1001 | 0.0896 | 0.0896 | 0.0896 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0917 | 0.0500 | 0.0500 | 0.0500 |
| phaseflip | phaseflip | 240 | 0.1844 | 0.1542 | 0.1658 | 0.1708 | 0.1708 | 0.1708 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0833 | 0.0625 | 0.0625 | 0.0625 |

## By Syndrome Observation Ratio

| syndrome_observation_ratio | cases | fid_gain_C1_mean | fid_gain_C2_mean | fid_gain_C3_mean | fid_gain_C3R_mean | false_safe_rate_C1 | false_safe_rate_C2 | false_safe_rate_C3 | false_safe_rate_C3R | false_safe_fidelity_rate_C1 | false_safe_fidelity_rate_C2 | false_safe_fidelity_rate_C3 | false_safe_fidelity_rate_C3R |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.0000 | 2400 | 0.1304 | 0.1273 | 0.1273 | 0.1273 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0521 | 0.0238 | 0.0238 | 0.0238 |

## By Syndrome Noise Probability

| syndrome_noise_prob | cases | fid_gain_C1_mean | fid_gain_C2_mean | fid_gain_C3_mean | fid_gain_C3R_mean | false_safe_rate_C1 | false_safe_rate_C2 | false_safe_rate_C3 | false_safe_rate_C3R | false_safe_fidelity_rate_C1 | false_safe_fidelity_rate_C2 | false_safe_fidelity_rate_C3 | false_safe_fidelity_rate_C3R |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | 2400 | 0.1304 | 0.1273 | 0.1273 | 0.1273 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0521 | 0.0238 | 0.0238 | 0.0238 |

## Preferred Policy By Regime Cell

| code_family | noise_family | noise_strength | noise_depth | cases | preferred_policy | preferred_fid_gain_mean | preferred_false_safe_fidelity_rate | preferred_false_safe_rate | preferred_chosen_B_rate | min_false_safe_rate | min_false_safe_fidelity_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bitflip | bitflip | 0.0100 | 1 | 10 | C1 | 0.0100 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | bitflip | 0.0100 | 2 | 10 | C1 | 0.0198 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | bitflip | 0.0100 | 3 | 10 | C1 | 0.0296 | 0.0000 | 0.0000 | 0.9000 | 0.0000 | 0.0000 |
| bitflip | bitflip | 0.0100 | 4 | 10 | C1 | 0.0392 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | bitflip | 0.0300 | 1 | 10 | C1 | 0.0300 | 0.0000 | 0.0000 | 0.9000 | 0.0000 | 0.0000 |
| bitflip | bitflip | 0.0300 | 2 | 10 | C1 | 0.0586 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | bitflip | 0.0300 | 3 | 10 | C1 | 0.0862 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | bitflip | 0.0300 | 4 | 10 | C1 | 0.1126 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | bitflip | 0.0500 | 1 | 10 | C1 | 0.0500 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | bitflip | 0.0500 | 2 | 10 | C1 | 0.0960 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | bitflip | 0.0500 | 3 | 10 | C1 | 0.1395 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | bitflip | 0.0500 | 4 | 10 | C1 | 0.1797 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | bitflip | 0.1000 | 1 | 10 | C1 | 0.1000 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | bitflip | 0.1000 | 2 | 10 | C1 | 0.1840 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | bitflip | 0.1000 | 3 | 10 | C1 | 0.2590 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | bitflip | 0.1000 | 4 | 10 | C1 | 0.3227 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | bitflip | 0.1500 | 1 | 10 | C1 | 0.1500 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | bitflip | 0.1500 | 2 | 10 | C1 | 0.2640 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | bitflip | 0.1500 | 3 | 10 | C1 | 0.3600 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | bitflip | 0.1500 | 4 | 10 | C1 | 0.4343 | 0.0000 | 0.0000 | 0.9000 | 0.0000 | 0.0000 |
| bitflip | bitflip | 0.2000 | 1 | 10 | C1 | 0.2000 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | bitflip | 0.2000 | 2 | 10 | C1 | 0.3360 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | bitflip | 0.2000 | 3 | 10 | C1 | 0.4440 | 0.0000 | 0.0000 | 0.9000 | 0.0000 | 0.0000 |
| bitflip | bitflip | 0.2000 | 4 | 10 | C1 | 0.5195 | 0.0000 | 0.0000 | 0.9000 | 0.0000 | 0.0000 |
| bitflip | dephasing | 0.0100 | 1 | 10 | C1 | 0.0050 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | dephasing | 0.0100 | 2 | 10 | C1 | 0.0099 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | dephasing | 0.0100 | 3 | 10 | C1 | 0.0149 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | dephasing | 0.0100 | 4 | 10 | C1 | 0.0197 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | dephasing | 0.0300 | 1 | 10 | C1 | 0.0150 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | dephasing | 0.0300 | 2 | 10 | C1 | 0.0295 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | dephasing | 0.0300 | 3 | 10 | C1 | 0.0437 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | dephasing | 0.0300 | 4 | 10 | C1 | 0.0574 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | dephasing | 0.0500 | 1 | 10 | C1 | 0.0250 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | dephasing | 0.0500 | 2 | 10 | C1 | 0.0487 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | dephasing | 0.0500 | 3 | 10 | C1 | 0.0713 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | dephasing | 0.0500 | 4 | 10 | C1 | 0.0927 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | dephasing | 0.1000 | 1 | 10 | C1 | 0.0500 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | dephasing | 0.1000 | 2 | 10 | C1 | 0.0950 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | dephasing | 0.1000 | 3 | 10 | C1 | 0.1355 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | dephasing | 0.1000 | 4 | 10 | C1 | 0.1720 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | dephasing | 0.1500 | 1 | 10 | C1 | 0.0750 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | dephasing | 0.1500 | 2 | 10 | C1 | 0.1387 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | dephasing | 0.1500 | 3 | 10 | C1 | 0.1929 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | dephasing | 0.1500 | 4 | 10 | C1 | 0.2390 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | dephasing | 0.2000 | 1 | 10 | C1 | 0.1000 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | dephasing | 0.2000 | 2 | 10 | C1 | 0.1800 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | dephasing | 0.2000 | 3 | 10 | C1 | 0.2440 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | dephasing | 0.2000 | 4 | 10 | C1 | 0.2952 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | depolarizing | 0.0100 | 1 | 10 | C1 | 0.0100 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | depolarizing | 0.0100 | 2 | 10 | C1 | 0.0199 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | depolarizing | 0.0100 | 3 | 10 | C1 | 0.0296 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | depolarizing | 0.0100 | 4 | 10 | C1 | 0.0367 | 0.0000 | 0.0000 | 0.9000 | 0.0000 | 0.0000 |
| bitflip | depolarizing | 0.0300 | 1 | 10 | C1 | 0.0300 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | depolarizing | 0.0300 | 2 | 10 | C1 | 0.0589 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | depolarizing | 0.0300 | 3 | 10 | C1 | 0.0868 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | depolarizing | 0.0300 | 4 | 10 | C1 | 0.0986 | 0.0000 | 0.0000 | 0.8000 | 0.0000 | 0.0000 |
| bitflip | depolarizing | 0.0500 | 1 | 10 | C1 | 0.0500 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | depolarizing | 0.0500 | 2 | 10 | C1 | 0.0969 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | depolarizing | 0.0500 | 3 | 10 | C1 | 0.1411 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | depolarizing | 0.0500 | 4 | 10 | C1 | 0.1827 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | depolarizing | 0.1000 | 1 | 10 | C1 | 0.1000 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | depolarizing | 0.1000 | 2 | 10 | C1 | 0.1752 | 0.0000 | 0.0000 | 0.9000 | 0.0000 | 0.0000 |
| bitflip | depolarizing | 0.1000 | 3 | 10 | C1 | 0.2653 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | depolarizing | 0.1000 | 4 | 10 | C1 | 0.3116 | 0.0000 | 0.0000 | 0.9000 | 0.0000 | 0.0000 |
| bitflip | depolarizing | 0.1500 | 1 | 10 | C1 | 0.1500 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | depolarizing | 0.1500 | 2 | 10 | C1 | 0.2720 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | depolarizing | 0.1500 | 3 | 10 | C1 | 0.3735 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | depolarizing | 0.1500 | 4 | 10 | C1 | 0.4566 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | depolarizing | 0.2000 | 1 | 10 | C1 | 0.2000 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | depolarizing | 0.2000 | 2 | 10 | C1 | 0.3502 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | depolarizing | 0.2000 | 3 | 10 | C1 | 0.4670 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | depolarizing | 0.2000 | 4 | 10 | C1 | 0.5555 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | mixed_pauli | 0.0100 | 1 | 10 | C1 | 0.0100 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | mixed_pauli | 0.0100 | 2 | 10 | C1 | 0.0192 | 0.0000 | 0.0000 | 0.9000 | 0.0000 | 0.0000 |
| bitflip | mixed_pauli | 0.0100 | 3 | 10 | C1 | 0.0296 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | mixed_pauli | 0.0100 | 4 | 10 | C1 | 0.0392 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | mixed_pauli | 0.0300 | 1 | 10 | C1 | 0.0300 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | mixed_pauli | 0.0300 | 2 | 10 | C1 | 0.0588 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | mixed_pauli | 0.0300 | 3 | 10 | C1 | 0.0750 | 0.0000 | 0.0000 | 0.8000 | 0.0000 | 0.0000 |
| bitflip | mixed_pauli | 0.0300 | 4 | 10 | C1 | 0.1131 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | mixed_pauli | 0.0500 | 1 | 10 | C1 | 0.0500 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | mixed_pauli | 0.0500 | 2 | 10 | C1 | 0.0968 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | mixed_pauli | 0.0500 | 3 | 10 | C1 | 0.1406 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | mixed_pauli | 0.0500 | 4 | 10 | C1 | 0.1812 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | mixed_pauli | 0.1000 | 1 | 10 | C1 | 0.1000 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | mixed_pauli | 0.1000 | 2 | 10 | C1 | 0.1872 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | mixed_pauli | 0.1000 | 3 | 10 | C1 | 0.2635 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | mixed_pauli | 0.1000 | 4 | 10 | C1 | 0.3041 | 0.0000 | 0.0000 | 0.9000 | 0.0000 | 0.0000 |
| bitflip | mixed_pauli | 0.1500 | 1 | 10 | C1 | 0.1500 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | mixed_pauli | 0.1500 | 2 | 10 | C1 | 0.2712 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | mixed_pauli | 0.1500 | 3 | 10 | C1 | 0.3698 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | mixed_pauli | 0.1500 | 4 | 10 | C1 | 0.4469 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | mixed_pauli | 0.2000 | 1 | 10 | C1 | 0.2000 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | mixed_pauli | 0.2000 | 2 | 10 | C1 | 0.3489 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | mixed_pauli | 0.2000 | 3 | 10 | C1 | 0.4609 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | mixed_pauli | 0.2000 | 4 | 10 | C1 | 0.5411 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | phaseflip | 0.0100 | 1 | 10 | C1 | 0.0100 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | phaseflip | 0.0100 | 2 | 10 | C1 | 0.0198 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | phaseflip | 0.0100 | 3 | 10 | C1 | 0.0294 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | phaseflip | 0.0100 | 4 | 10 | C1 | 0.0388 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | phaseflip | 0.0300 | 1 | 10 | C1 | 0.0300 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | phaseflip | 0.0300 | 2 | 10 | C1 | 0.0582 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | phaseflip | 0.0300 | 3 | 10 | C1 | 0.0847 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | phaseflip | 0.0300 | 4 | 10 | C1 | 0.1096 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | phaseflip | 0.0500 | 1 | 10 | C1 | 0.0500 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | phaseflip | 0.0500 | 2 | 10 | C1 | 0.0950 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | phaseflip | 0.0500 | 3 | 10 | C1 | 0.1355 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | phaseflip | 0.0500 | 4 | 10 | C1 | 0.1720 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | phaseflip | 0.1000 | 1 | 10 | C1 | 0.1000 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | phaseflip | 0.1000 | 2 | 10 | C1 | 0.1800 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | phaseflip | 0.1000 | 3 | 10 | C1 | 0.2440 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | phaseflip | 0.1000 | 4 | 10 | C1 | 0.2952 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | phaseflip | 0.1500 | 1 | 10 | C1 | 0.1500 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | phaseflip | 0.1500 | 2 | 10 | C1 | 0.2550 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | phaseflip | 0.1500 | 3 | 10 | C1 | 0.3285 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | phaseflip | 0.1500 | 4 | 10 | C1 | 0.3799 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | phaseflip | 0.2000 | 1 | 10 | C1 | 0.2000 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | phaseflip | 0.2000 | 2 | 10 | C1 | 0.3200 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | phaseflip | 0.2000 | 3 | 10 | C1 | 0.3920 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| bitflip | phaseflip | 0.2000 | 4 | 10 | C1 | 0.4352 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| phaseflip | bitflip | 0.0100 | 1 | 10 | C1 | -0.0202 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | 1.0000 |
| phaseflip | bitflip | 0.0100 | 2 | 10 | C2 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| phaseflip | bitflip | 0.0100 | 3 | 10 | C2 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| phaseflip | bitflip | 0.0100 | 4 | 10 | C1 | 0.0087 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| phaseflip | bitflip | 0.0300 | 1 | 10 | C1 | -0.0002 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| phaseflip | bitflip | 0.0300 | 2 | 10 | C1 | 0.0280 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| phaseflip | bitflip | 0.0300 | 3 | 10 | C1 | 0.0546 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| phaseflip | bitflip | 0.0300 | 4 | 10 | C1 | 0.0795 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| phaseflip | bitflip | 0.0500 | 1 | 10 | C1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| phaseflip | bitflip | 0.0500 | 2 | 10 | C1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| phaseflip | bitflip | 0.0500 | 3 | 10 | C1 | -0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| phaseflip | bitflip | 0.0500 | 4 | 10 | C1 | 0.1418 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| phaseflip | bitflip | 0.1000 | 1 | 10 | C1 | 0.0698 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| phaseflip | bitflip | 0.1000 | 2 | 10 | C1 | -0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| phaseflip | bitflip | 0.1000 | 3 | 10 | C1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| phaseflip | bitflip | 0.1000 | 4 | 10 | C1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| phaseflip | bitflip | 0.1500 | 1 | 10 | C1 | -0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| phaseflip | bitflip | 0.1500 | 2 | 10 | C1 | -0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| phaseflip | bitflip | 0.1500 | 3 | 10 | C1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| phaseflip | bitflip | 0.1500 | 4 | 10 | C1 | 0.3498 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| phaseflip | bitflip | 0.2000 | 1 | 10 | C1 | 0.1698 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| phaseflip | bitflip | 0.2000 | 2 | 10 | C1 | -0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| phaseflip | bitflip | 0.2000 | 3 | 10 | C1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| phaseflip | bitflip | 0.2000 | 4 | 10 | C1 | 0.2430 | 0.0000 | 0.0000 | 0.6000 | 0.0000 | 0.0000 |
| phaseflip | dephasing | 0.0100 | 1 | 10 | C2 | -0.0191 | 0.8000 | 0.0000 | 0.8000 | 0.0000 | 0.8000 |
| phaseflip | dephasing | 0.0100 | 2 | 10 | C2 | -0.0051 | 0.5000 | 0.0000 | 0.5000 | 0.0000 | 0.5000 |
| phaseflip | dephasing | 0.0100 | 3 | 10 | C2 | 0.0028 | 0.4000 | 0.0000 | 0.4000 | 0.0000 | 0.4000 |
| phaseflip | dephasing | 0.0100 | 4 | 10 | C2 | 0.0138 | 0.2000 | 0.0000 | 0.2000 | 0.0000 | 0.2000 |
| phaseflip | dephasing | 0.0300 | 1 | 10 | C2 | 0.0120 | 0.1000 | 0.0000 | 0.1000 | 0.0000 | 0.1000 |
| phaseflip | dephasing | 0.0300 | 2 | 10 | C2 | 0.0206 | 0.0000 | 0.0000 | 0.3000 | 0.0000 | 0.0000 |
| phaseflip | dephasing | 0.0300 | 3 | 10 | C2 | 0.0350 | 0.0000 | 0.0000 | 0.3000 | 0.0000 | 0.0000 |
| phaseflip | dephasing | 0.0300 | 4 | 10 | C2 | 0.0491 | 0.0000 | 0.0000 | 0.3000 | 0.0000 | 0.0000 |
| phaseflip | dephasing | 0.0500 | 1 | 10 | C2 | 0.0009 | 0.0000 | 0.0000 | 0.8000 | 0.0000 | 0.0000 |
| phaseflip | dephasing | 0.0500 | 2 | 10 | C2 | 0.0339 | 0.0000 | 0.0000 | 0.5000 | 0.0000 | 0.0000 |
| phaseflip | dephasing | 0.0500 | 3 | 10 | C2 | 0.0573 | 0.0000 | 0.0000 | 0.5000 | 0.0000 | 0.0000 |
| phaseflip | dephasing | 0.0500 | 4 | 10 | C2 | 0.0827 | 0.0000 | 0.0000 | 0.4000 | 0.0000 | 0.0000 |
| phaseflip | dephasing | 0.1000 | 1 | 10 | C2 | 0.0259 | 0.0000 | 0.0000 | 0.8000 | 0.0000 | 0.0000 |
| phaseflip | dephasing | 0.1000 | 2 | 10 | C2 | 0.0900 | 0.0000 | 0.0000 | 0.2000 | 0.0000 | 0.0000 |
| phaseflip | dephasing | 0.1000 | 3 | 10 | C1 | 0.1274 | 0.0000 | 0.0000 | 0.4000 | 0.0000 | 0.0000 |
| phaseflip | dephasing | 0.1000 | 4 | 10 | C1 | 0.1737 | 0.0000 | 0.0000 | 0.2000 | 0.0000 | 0.0000 |
| phaseflip | dephasing | 0.1500 | 1 | 10 | C2 | 0.0599 | 0.0000 | 0.0000 | 0.5000 | 0.0000 | 0.0000 |
| phaseflip | dephasing | 0.1500 | 2 | 10 | C1 | 0.1229 | 0.0000 | 0.0000 | 0.6000 | 0.0000 | 0.0000 |
| phaseflip | dephasing | 0.1500 | 3 | 10 | C1 | 0.1956 | 0.0000 | 0.0000 | 0.2000 | 0.0000 | 0.0000 |
| phaseflip | dephasing | 0.1500 | 4 | 10 | C1 | 0.2555 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| phaseflip | dephasing | 0.2000 | 1 | 10 | C2 | 0.0940 | 0.0000 | 0.0000 | 0.2000 | 0.0000 | 0.0000 |
| phaseflip | dephasing | 0.2000 | 2 | 10 | C1 | 0.1750 | 0.0000 | 0.0000 | 0.3000 | 0.0000 | 0.0000 |
| phaseflip | dephasing | 0.2000 | 3 | 10 | C1 | 0.2500 | 0.0000 | 0.0000 | 0.3000 | 0.0000 | 0.0000 |
| phaseflip | dephasing | 0.2000 | 4 | 10 | C1 | 0.3137 | 0.0000 | 0.0000 | 0.3000 | 0.0000 | 0.0000 |
| phaseflip | depolarizing | 0.0100 | 1 | 10 | C2 | 0.0034 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| phaseflip | depolarizing | 0.0100 | 2 | 10 | C2 | 0.0066 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| phaseflip | depolarizing | 0.0100 | 3 | 10 | C2 | 0.0101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| phaseflip | depolarizing | 0.0100 | 4 | 10 | C2 | 0.0128 | 0.0000 | 0.0000 | 0.1000 | 0.0000 | 0.0000 |
| phaseflip | depolarizing | 0.0300 | 1 | 10 | C2 | 0.0079 | 0.0000 | 0.0000 | 0.2000 | 0.0000 | 0.0000 |
| phaseflip | depolarizing | 0.0300 | 2 | 10 | C1 | 0.0287 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| phaseflip | depolarizing | 0.0300 | 3 | 10 | C1 | 0.0566 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| phaseflip | depolarizing | 0.0300 | 4 | 10 | C1 | 0.0835 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| phaseflip | depolarizing | 0.0500 | 1 | 10 | C2 | 0.0167 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| phaseflip | depolarizing | 0.0500 | 2 | 10 | C1 | 0.0667 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| phaseflip | depolarizing | 0.0500 | 3 | 10 | C1 | 0.1047 | 0.0000 | 0.0000 | 0.9000 | 0.0000 | 0.0000 |
| phaseflip | depolarizing | 0.0500 | 4 | 10 | C1 | 0.0797 | 0.0000 | 0.0000 | 0.2000 | 0.0000 | 0.0000 |
| phaseflip | depolarizing | 0.1000 | 1 | 10 | C1 | 0.0661 | 0.0000 | 0.0000 | 0.9000 | 0.0000 | 0.0000 |
| phaseflip | depolarizing | 0.1000 | 2 | 10 | C1 | 0.0624 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| phaseflip | depolarizing | 0.1000 | 3 | 10 | C1 | 0.0904 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| phaseflip | depolarizing | 0.1000 | 4 | 10 | C1 | 0.1529 | 0.0000 | 0.0000 | 0.2000 | 0.0000 | 0.0000 |
| phaseflip | depolarizing | 0.1500 | 1 | 10 | C1 | 0.0568 | 0.0000 | 0.0000 | 0.1000 | 0.0000 | 0.0000 |
| phaseflip | depolarizing | 0.1500 | 2 | 10 | C1 | 0.1062 | 0.0000 | 0.0000 | 0.1000 | 0.0000 | 0.0000 |
| phaseflip | depolarizing | 0.1500 | 3 | 10 | C1 | 0.1300 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| phaseflip | depolarizing | 0.1500 | 4 | 10 | C1 | 0.1869 | 0.0000 | 0.0000 | 0.1000 | 0.0000 | 0.0000 |
| phaseflip | depolarizing | 0.2000 | 1 | 10 | C1 | 0.0662 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| phaseflip | depolarizing | 0.2000 | 2 | 10 | C1 | 0.1198 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| phaseflip | depolarizing | 0.2000 | 3 | 10 | C1 | 0.2731 | 0.0000 | 0.0000 | 0.4000 | 0.0000 | 0.0000 |
| phaseflip | depolarizing | 0.2000 | 4 | 10 | C1 | 0.2654 | 0.0000 | 0.0000 | 0.2000 | 0.0000 | 0.0000 |
| phaseflip | mixed_pauli | 0.0100 | 1 | 10 | C2 | -0.0186 | 0.9000 | 0.0000 | 0.9000 | 0.0000 | 0.9000 |
| phaseflip | mixed_pauli | 0.0100 | 2 | 10 | C2 | 0.0004 | 0.3000 | 0.0000 | 0.3000 | 0.0000 | 0.3000 |
| phaseflip | mixed_pauli | 0.0100 | 3 | 10 | C2 | 0.0057 | 0.0000 | 0.0000 | 0.4000 | 0.0000 | 0.0000 |
| phaseflip | mixed_pauli | 0.0100 | 4 | 10 | C2 | 0.0150 | 0.0000 | 0.0000 | 0.2000 | 0.0000 | 0.0000 |
| phaseflip | mixed_pauli | 0.0300 | 1 | 10 | C2 | 0.0074 | 0.0000 | 0.0000 | 0.6000 | 0.0000 | 0.0000 |
| phaseflip | mixed_pauli | 0.0300 | 2 | 10 | C2 | 0.0245 | 0.0000 | 0.0000 | 0.6000 | 0.0000 | 0.0000 |
| phaseflip | mixed_pauli | 0.0300 | 3 | 10 | C2 | 0.0401 | 0.0000 | 0.0000 | 0.4000 | 0.0000 | 0.0000 |
| phaseflip | mixed_pauli | 0.0300 | 4 | 10 | C1 | 0.0712 | 0.0000 | 0.0000 | 0.9000 | 0.0000 | 0.0000 |
| phaseflip | mixed_pauli | 0.0500 | 1 | 10 | C2 | 0.0085 | 0.0000 | 0.0000 | 0.3000 | 0.0000 | 0.0000 |
| phaseflip | mixed_pauli | 0.0500 | 2 | 10 | C2 | 0.0410 | 0.0000 | 0.0000 | 0.5000 | 0.0000 | 0.0000 |
| phaseflip | mixed_pauli | 0.0500 | 3 | 10 | C1 | 0.0957 | 0.0000 | 0.0000 | 0.9000 | 0.0000 | 0.0000 |
| phaseflip | mixed_pauli | 0.0500 | 4 | 10 | C1 | 0.1092 | 0.0000 | 0.0000 | 0.7000 | 0.0000 | 0.0000 |
| phaseflip | mixed_pauli | 0.1000 | 1 | 10 | C1 | 0.0548 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| phaseflip | mixed_pauli | 0.1000 | 2 | 10 | C1 | 0.0802 | 0.0000 | 0.0000 | 0.3000 | 0.0000 | 0.0000 |
| phaseflip | mixed_pauli | 0.1000 | 3 | 10 | C1 | 0.1839 | 0.0000 | 0.0000 | 0.6000 | 0.0000 | 0.0000 |
| phaseflip | mixed_pauli | 0.1000 | 4 | 10 | C1 | 0.1834 | 0.0000 | 0.0000 | 0.3000 | 0.0000 | 0.0000 |
| phaseflip | mixed_pauli | 0.1500 | 1 | 10 | C1 | 0.0404 | 0.0000 | 0.0000 | 0.4000 | 0.0000 | 0.0000 |
| phaseflip | mixed_pauli | 0.1500 | 2 | 10 | C1 | 0.1235 | 0.0000 | 0.0000 | 0.2000 | 0.0000 | 0.0000 |
| phaseflip | mixed_pauli | 0.1500 | 3 | 10 | C1 | 0.1782 | 0.0000 | 0.0000 | 0.1000 | 0.0000 | 0.0000 |
| phaseflip | mixed_pauli | 0.1500 | 4 | 10 | C1 | 0.2073 | 0.0000 | 0.0000 | 0.1000 | 0.0000 | 0.0000 |
| phaseflip | mixed_pauli | 0.2000 | 1 | 10 | C1 | 0.1398 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| phaseflip | mixed_pauli | 0.2000 | 2 | 10 | C1 | 0.1780 | 0.0000 | 0.0000 | 0.3000 | 0.0000 | 0.0000 |
| phaseflip | mixed_pauli | 0.2000 | 3 | 10 | C1 | 0.3135 | 0.0000 | 0.0000 | 0.5000 | 0.0000 | 0.0000 |
| phaseflip | mixed_pauli | 0.2000 | 4 | 10 | C1 | 0.3698 | 0.0000 | 0.0000 | 0.6000 | 0.0000 | 0.0000 |
| phaseflip | phaseflip | 0.0100 | 1 | 10 | C2 | -0.0111 | 0.7000 | 0.0000 | 0.7000 | 0.0000 | 0.7000 |
| phaseflip | phaseflip | 0.0100 | 2 | 10 | C2 | -0.0043 | 0.8000 | 0.0000 | 0.8000 | 0.0000 | 0.8000 |
| phaseflip | phaseflip | 0.0100 | 3 | 10 | C2 | 0.0085 | 0.0000 | 0.0000 | 0.7000 | 0.0000 | 0.0000 |
| phaseflip | phaseflip | 0.0100 | 4 | 10 | C2 | 0.0241 | 0.0000 | 0.0000 | 0.5000 | 0.0000 | 0.0000 |
| phaseflip | phaseflip | 0.0300 | 1 | 10 | C2 | 0.0059 | 0.0000 | 0.0000 | 0.8000 | 0.0000 | 0.0000 |
| phaseflip | phaseflip | 0.0300 | 2 | 10 | C2 | 0.0435 | 0.0000 | 0.0000 | 0.5000 | 0.0000 | 0.0000 |
| phaseflip | phaseflip | 0.0300 | 3 | 10 | C2 | 0.0651 | 0.0000 | 0.0000 | 0.7000 | 0.0000 | 0.0000 |
| phaseflip | phaseflip | 0.0300 | 4 | 10 | C1 | 0.1005 | 0.0000 | 0.0000 | 0.4000 | 0.0000 | 0.0000 |
| phaseflip | phaseflip | 0.0500 | 1 | 10 | C2 | 0.0259 | 0.0000 | 0.0000 | 0.8000 | 0.0000 | 0.0000 |
| phaseflip | phaseflip | 0.0500 | 2 | 10 | C2 | 0.0900 | 0.0000 | 0.0000 | 0.2000 | 0.0000 | 0.0000 |
| phaseflip | phaseflip | 0.0500 | 3 | 10 | C1 | 0.1305 | 0.0000 | 0.0000 | 0.3000 | 0.0000 | 0.0000 |
| phaseflip | phaseflip | 0.0500 | 4 | 10 | C1 | 0.1737 | 0.0000 | 0.0000 | 0.2000 | 0.0000 | 0.0000 |
| phaseflip | phaseflip | 0.1000 | 1 | 10 | C2 | 0.0940 | 0.0000 | 0.0000 | 0.2000 | 0.0000 | 0.0000 |
| phaseflip | phaseflip | 0.1000 | 2 | 10 | C1 | 0.1750 | 0.0000 | 0.0000 | 0.3000 | 0.0000 | 0.0000 |
| phaseflip | phaseflip | 0.1000 | 3 | 10 | C1 | 0.2530 | 0.0000 | 0.0000 | 0.2000 | 0.0000 | 0.0000 |
| phaseflip | phaseflip | 0.1000 | 4 | 10 | C1 | 0.3137 | 0.0000 | 0.0000 | 0.3000 | 0.0000 | 0.0000 |
| phaseflip | phaseflip | 0.1500 | 1 | 10 | C1 | 0.1349 | 0.0000 | 0.0000 | 0.5000 | 0.0000 | 0.0000 |
| phaseflip | phaseflip | 0.1500 | 2 | 10 | C1 | 0.2429 | 0.0000 | 0.0000 | 0.7000 | 0.0000 | 0.0000 |
| phaseflip | phaseflip | 0.1500 | 3 | 10 | C1 | 0.3570 | 0.0000 | 0.0000 | 0.1000 | 0.0000 | 0.0000 |
| phaseflip | phaseflip | 0.1500 | 4 | 10 | C1 | 0.4343 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| phaseflip | phaseflip | 0.2000 | 1 | 10 | C1 | 0.1789 | 0.0000 | 0.0000 | 0.7000 | 0.0000 | 0.0000 |
| phaseflip | phaseflip | 0.2000 | 2 | 10 | C1 | 0.3058 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| phaseflip | phaseflip | 0.2000 | 3 | 10 | C1 | 0.4380 | 0.0000 | 0.0000 | 0.2000 | 0.0000 | 0.0000 |
| phaseflip | phaseflip | 0.2000 | 4 | 10 | C1 | 0.5195 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## Preferred Policy Summary

| preferred_policy | cases | preferred_policy_rate | mean_preferred_fid_gain | mean_preferred_false_safe_fidelity_rate | mean_preferred_false_safe_rate |
| --- | --- | --- | --- | --- | --- |
| C1 | 197 | 1.0000 | 0.1559 | 0.0051 | 0.0000 |
| C2 | 43 | 1.0000 | 0.0250 | 0.1093 | 0.0000 |

## C3R Switch Intervention Quality

| c2_B_count | c3r_block_count | c3r_block_rate_given_c2_B | c3r_harmful_block_precision | c3r_harmful_switch_recall | c3r_beneficial_switch_block_rate | c3r_beneficial_switch_retention | c3r_prevented_loss_sum | c3r_missed_gain_sum | c3r_net_intervention_gain | c3r_intervention_gain_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1529 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## Tail Risk and Oracle Diagnostics

| fid_gain_q05_C2 | fid_gain_q05_C3R | fid_gain_cvar05_C2 | fid_gain_cvar05_C3R | observed_failure_boundary_rate_C2 | observed_failure_boundary_rate_C3R | true_failure_boundary_rate_C2 | true_failure_boundary_rate_C3R | chosen_candidate_violation_mean_C2 | chosen_candidate_violation_mean_C3R | admissible_rate_C2 | admissible_rate_C3R | oracle_regret_mean_C2 | oracle_regret_mean_C3R | oracle_regret_q95_C2 | oracle_regret_q95_C3R |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| -0.0000 | -0.0000 | -0.0033 | -0.0033 | 0.2571 | 0.2571 | 0.2571 | 0.2571 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 0.0297 | 0.0297 | 0.2131 | 0.2131 |

## C3R By Raw Uncertainty Bin

| c3r_raw_syndrome_uncertainty_bin | cases | c2_B_count | c3r_block_count | c3r_block_rate_given_c2_B | c3r_harmful_block_precision | c3r_harmful_switch_recall | c3r_beneficial_switch_block_rate | c3r_net_intervention_gain |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [0.00,0.25) | 2400 | 1529 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## Decision Reasons

| mode | reason | count | rate |
| --- | --- | --- | --- |
| C1 | keep_syndrome | 484 | 0.2017 |
| C1 | tie_break_objective | 387 | 0.1613 |
| C1 | veto_nonadmissible_A | 1529 | 0.6371 |
| C2 | inadmissibility_penalty_triggered | 1529 | 0.6371 |
| C2 | score_prefers_A | 871 | 0.3629 |
| C3 | hard_inadmissibility_block | 1529 | 0.6371 |
| C3 | safety_prefers_A | 871 | 0.3629 |
| C3R | c3r_all_gates_pass_switch_to_B | 1529 | 0.6371 |
| C3R | c3r_c2_preserves_A | 871 | 0.3629 |

## Figures

- `hybrid_c123_fid_gain_comparison`: `D:\Pandora_box\biqmn\results\plots\hybrid_c123_regime_map_c3r_260427_seed10_fid_gain_comparison.png`
- `hybrid_c123_false_safe_comparison`: `D:\Pandora_box\biqmn\results\plots\hybrid_c123_regime_map_c3r_260427_seed10_false_safe_comparison.png`
- `hybrid_c123_reason_composition`: `D:\Pandora_box\biqmn\results\plots\hybrid_c123_regime_map_c3r_260427_seed10_reason_composition.png`
- `hybrid_c123_tradeoff_frontier`: `D:\Pandora_box\biqmn\results\plots\hybrid_c123_regime_map_c3r_260427_seed10_tradeoff_frontier.png`
- `hybrid_c123_regime_boundary_map`: `D:\Pandora_box\biqmn\results\plots\hybrid_c123_regime_map_c3r_260427_seed10_regime_boundary_map.png`
