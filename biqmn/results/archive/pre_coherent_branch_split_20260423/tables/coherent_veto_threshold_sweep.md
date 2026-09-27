# Coherent Veto Threshold Sweep

## Operating Points

| mode | scope | threshold_quantile | threshold | risky_case_capture_rate | safe_case_retention_rate | abstain_rate | false_safe_rate_after_veto | accepted_false_safe_rate | selection_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V1 | overall | 0.7000 | 0.9041 | 0.1881 | 0.5978 | 0.0000 | 0.6486 | 0.9396 | 0.1373 |
| V2 | overall | 0.9500 | 1.8229 | 0.0000 | 0.9108 | 0.0507 | 0.9076 | 0.9561 | -1.0037 |

## Overall Threshold Sweep

| mode | threshold_quantile | threshold | flag_rate | risky_case_capture_rate | safe_case_retention_rate | abstain_rate | false_safe_rate_after_veto | accepted_false_safe_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V1 | 0.7000 | 0.9041 | 0.3097 | 0.1881 | 0.5978 | 0.0000 | 0.6486 | 0.9396 |
| V2 | 0.7000 | 0.9041 | 0.3097 | 0.1881 | 0.5978 | 0.3097 | 0.6486 | 0.9396 |
| V1 | 0.8000 | 1.2130 | 0.2153 | 0.0756 | 0.6785 | 0.0000 | 0.7431 | 0.9469 |
| V2 | 0.8000 | 1.2130 | 0.2153 | 0.0756 | 0.6785 | 0.2153 | 0.7431 | 0.9469 |
| V1 | 0.9000 | 1.8190 | 0.1035 | 0.0096 | 0.8252 | 0.0000 | 0.8549 | 0.9535 |
| V2 | 0.9000 | 1.8190 | 0.1035 | 0.0096 | 0.8252 | 0.1035 | 0.8549 | 0.9535 |
| V1 | 0.9500 | 1.8229 | 0.0507 | 0.0000 | 0.9108 | 0.0000 | 0.9076 | 0.9561 |
| V2 | 0.9500 | 1.8229 | 0.0507 | 0.0000 | 0.9108 | 0.0507 | 0.9076 | 0.9561 |

## False-Safe Comparison

| scope | cases | false_safe_rate_A | V1_threshold_quantile | V1_false_safe_after_flag | V2_threshold_quantile | V2_false_safe_after_abstain | V2_abstain_rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| overall | 1440 | 0.9569 | 0.7000 | 0.6486 | 0.9500 | 0.9561 | 0.0507 |
| bitflip/coherent_x | 720 | 0.9556 | 0.7000 | 0.6375 | 0.9500 | 0.9559 | 0.0556 |
| phaseflip/coherent_z | 720 | 0.9583 | 0.7000 | 0.6597 | 0.9500 | 0.9563 | 0.0458 |

## Figures

- `figure_b_threshold_sweep`: `D:\pandora_box\biqmn\results\plots\coherent_veto_threshold_sweep_threshold_sweep.png`
- `figure_c_false_safe_before_after`: `D:\pandora_box\biqmn\results\plots\coherent_veto_threshold_sweep_false_safe_before_after.png`
