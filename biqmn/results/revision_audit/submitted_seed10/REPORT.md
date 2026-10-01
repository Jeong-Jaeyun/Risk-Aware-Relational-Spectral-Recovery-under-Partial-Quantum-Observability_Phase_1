# Submitted-result audit

Generated from immutable 260427 seed10 raw JSON files.

Intervals: paired whole-seed percentile bootstrap, conditional on the fixed grids. Only 10 seed blocks; no claim of out-of-grid generalization or confirmatory significance.

| Regime | Rows | C2 proposes B | C3R blocks | Score/admissibility-only blocks | B admissible |
|---|---:|---:|---:|---:|---:|
| Clean | 2400 | 1529 | 0 | 0 | 2400 |
| Partial | 2880 | 1094 | 476 | 0 | 2880 |
| Noisy-only | 3600 | 1370 | 0 | 0 | 3600 |
| Partial-plus-noisy | 2160 | 821 | 670 | 0 | 2160 |
| Ambiguity-plus-measurement | 3600 | 895 | 357 | 0 | 3600 |

## Paired C3R minus C2 differences

False-safe differences below are percentage points. Positive mean/tail gain is favorable; negative false-safe and regret is favorable.

| Regime | Metric | Estimate | 95% seed bootstrap CI |
|---|---|---:|---|
| Clean | mean_gain | 0 | [0, 0] |
| Clean | false_safe_rate | 0 | [0, 0] |
| Clean | q05_gain | 0 | [0, 0] |
| Clean | lower_tail_mean_paper | 0 | [0, 0] |
| Clean | cvar05_exact_mass | 0 | [0, 0] |
| Clean | mean_oracle_regret | 0 | [0, 0] |
| Partial | mean_gain | 0.00196582 | [0.000528519, 0.00346726] |
| Partial | false_safe_rate | -3.05556 | [-3.47222, -2.63889] |
| Partial | q05_gain | 0.0146494 | [0.009848, 0.01505] |
| Partial | lower_tail_mean_paper | 0.00615537 | [0.0045209, 0.00974785] |
| Partial | cvar05_exact_mass | 0.00631121 | [0.0041772, 0.00842305] |
| Partial | mean_oracle_regret | -0.00196582 | [-0.00346726, -0.000528519] |
| Noisy-only | mean_gain | 0 | [0, 0] |
| Noisy-only | false_safe_rate | 0 | [0, 0] |
| Noisy-only | q05_gain | 0 | [0, 0] |
| Noisy-only | lower_tail_mean_paper | 0 | [0, 0] |
| Noisy-only | cvar05_exact_mass | 0 | [0, 0] |
| Noisy-only | mean_oracle_regret | 0 | [0, 0] |
| Partial-plus-noisy | mean_gain | 0.00422276 | [0.00122402, 0.00716864] |
| Partial-plus-noisy | false_safe_rate | -5.50926 | [-6.57407, -4.39815] |
| Partial-plus-noisy | q05_gain | 0.0103586 | [0.0103537, 0.0154517] |
| Partial-plus-noisy | lower_tail_mean_paper | 0.0171944 | [0.010043, 0.0215273] |
| Partial-plus-noisy | cvar05_exact_mass | 0.0153912 | [0.00821395, 0.0217719] |
| Partial-plus-noisy | mean_oracle_regret | -0.00422276 | [-0.00716864, -0.00122402] |
| Ambiguity-plus-measurement | mean_gain | 0.000437463 | [-0.000973686, 0.00185948] |
| Ambiguity-plus-measurement | false_safe_rate | 0 | [0, 0] |
| Ambiguity-plus-measurement | q05_gain | 0.00452869 | [0, 0.0240349] |
| Ambiguity-plus-measurement | lower_tail_mean_paper | 0.000599167 | [-0.00229249, 0.00822341] |
| Ambiguity-plus-measurement | cvar05_exact_mass | 0.000223873 | [0, 0.00560639] |
| Ambiguity-plus-measurement | mean_oracle_regret | -0.000437463 | [-0.00185948, 0.000973686] |

The original tail mean averages every observation at/below q05 (with tolerance 1e-12). With ties this may contain more than 5% of the mass. cvar05_exact_mass is reported as a sensitivity definition; the original values are preserved.

## Structural checks

See structural_checks.json for numeric evidence and source_manifest.json for hashes.

- bitflip: clock overlap minimum 1; maximum slice change 3.19e-16; constraint residual 0.8; kernel dimension 0.
- phaseflip: clock overlap minimum 1; maximum slice change 3.51e-16; constraint residual 0.8; kernel dimension 0.

With |+> and H_C=0.8 X, clock kets differ only by global phase. The projector and all normalized conditional slices are constant for any fixed joint density. The cosine-overlap formula applies to a different initial clock state.

Encoded preparation uses c0|0>|0_L> + c1|1>|1_L>; H_S=0, so the submitted encoded state is not a zero-energy Page-Wootters state. Candidate A uses the complete syndrome recovery channel on each density; degraded observations affect the controller, not A's correction channel. These are substantive scope limitations, not just missing equations.

The retained C2 proposal and candidate B still use relational features. Equivalence of the extra uncertainty veto does not prove that the entire pipeline is independent of those features. Candidate-generation baselines are evaluated separately.
