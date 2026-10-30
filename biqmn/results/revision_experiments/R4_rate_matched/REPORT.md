# R4 equal-coverage and continuous-estimator audit

Reviewer-prompted secondary analysis of the existing R3 streams. No new count realizations.

Intervals are pointwise paired two-way cluster bootstrap intervals, conditional on the R3 banks and thresholds.

## Stream aggregate at 50% of C2 proposals

| Stream | Policy | Harm among accepted | Mean fidelity | Gain vs A*_all [95% CI] |
|---|---|---:|---:|---|
| 0 | random | 65.546% | 0.957354 | -0.024223 [-0.027523, -0.020699] |
| 0 | score | 56.261% | 0.962726 | -0.018851 [-0.022653, -0.015618] |
| 0 | U | 66.384% | 0.958786 | -0.022791 [-0.025910, -0.019751] |
| 0 | H | 45.608% | 0.969628 | -0.011949 [-0.016003, -0.008462] |
| 0 | C3R | 63.104% | 0.960967 | -0.020610 [-0.023522, -0.017875] |
| 1 | random | 56.884% | 0.962354 | -0.019500 [-0.022861, -0.016103] |
| 1 | score | 47.907% | 0.966375 | -0.015480 [-0.018329, -0.013455] |
| 1 | U | 58.427% | 0.963116 | -0.018738 [-0.021615, -0.015941] |
| 1 | H | 36.671% | 0.972885 | -0.008970 [-0.012445, -0.005798] |
| 1 | C3R | 57.547% | 0.963819 | -0.018035 [-0.020686, -0.015391] |
| 2 | random | 51.745% | 0.964166 | -0.018215 [-0.021226, -0.015228] |
| 2 | score | 42.379% | 0.966354 | -0.016027 [-0.018404, -0.013947] |
| 2 | U | 51.538% | 0.964903 | -0.017478 [-0.020176, -0.014918] |
| 2 | H | 27.858% | 0.972381 | -0.010000 [-0.013360, -0.007068] |
| 2 | C3R | 48.132% | 0.966142 | -0.016239 [-0.018629, -0.013822] |
| 3 | random | 53.967% | 0.958868 | -0.022316 [-0.026985, -0.017721] |
| 3 | score | 42.223% | 0.965658 | -0.015526 [-0.018620, -0.013420] |
| 3 | U | 54.246% | 0.961545 | -0.019639 [-0.023315, -0.016241] |
| 3 | H | 30.751% | 0.971692 | -0.009492 [-0.013501, -0.006113] |
| 3 | C3R | 53.052% | 0.962336 | -0.018848 [-0.022175, -0.015643] |

## Original fixed gates at common expected coverage

| Stream | Informative cells | H minus random harm [95% CI], pp | C3R minus U harm [95% CI], pp |
|---|---:|---|---|
| 0 | 12/24 | -7.616 [-10.263, -5.421] | -5.225 [-7.565, -3.317] |
| 1 | 12/24 | -3.000 [-4.358, -1.811] | -1.459 [-2.388, -0.694] |
| 2 | 12/24 | -6.194 [-9.481, -3.883] | -4.370 [-7.054, -2.454] |
| 3 | 12/24 | -4.476 [-7.039, -2.609] | -1.928 [-3.263, -0.979] |

Full cell results, all three retention levels, controls, tails, intervals, and replay checks are in summary.json.
The ranking curves use observed batch diagnostics without target outcomes. They are not calibration-only deployment rules.
Tail summaries use per-record mixtures; R3 tail metrics use a different seed-averaged unit.
