# R4 results and supported scope

R4 and its separate harm-margin follow-up are secondary analyses of the four
existing R3 streams. They introduce no new count realizations or independent
replications. All 24 cells per stream are retained; the two code conventions
are coupled checks. Intervals are paired pointwise two-way cluster bootstrap
intervals, conditional on the fixed model, grid, bank, and calibration.

## Equal expected switching rates

The original fixed gates are compared after random thinning to C3R's expected
switch count. At 256 copies this common count is zero, so conditional switch
quality is uninformative. In the twelve active 1,024-copy cells per stream,
H minus random retention of C2 has mean conditional-harm differences of
-7.62, -3.00, -6.19, and -4.48 percentage points. C3R minus U has differences
of -5.23, -1.46, -4.37, and -1.93 points. All eight intervals exclude zero.

Separate batch rankings retain 25%, 50%, or 75% of the original C2 proposals.
They use observed diagnostics without target outcomes and integrate boundary
ties analytically. They are not calibration-only deployment policies.
At 50% retention, H minus U is:

| Stream | Conditional harm, numerical tolerance, pp [95% CI] | Conditional harm, margin 0.01, pp [95% CI] | Overall mean fidelity [95% CI] |
|---|---|---|---|
| r0 | -20.78 [-24.88, -16.24] | -26.60 [-30.53, -21.41] | +0.01084 [+0.00898, +0.01275] |
| r1 | -21.76 [-25.48, -17.00] | -24.08 [-27.20, -19.45] | +0.00977 [+0.00811, +0.01141] |
| r2 | -23.68 [-26.55, -19.41] | -23.80 [-26.98, -18.55] | +0.00748 [+0.00605, +0.00879] |
| r3 | -23.50 [-26.59, -19.14] | -25.24 [-29.72, -17.97] | +0.01015 [+0.00815, +0.01197] |

Harm is defined by F_B < F_A - epsilon. All margins
epsilon = 1e-12, 0.001, 0.005, and 0.01 are reported. Policies remain fixed;
only evaluator labels change. Positive margins are sensitivity choices, not
application-validated utility thresholds. The mean-fidelity comparison retains
all signed gains and losses, including those inside a margin.

The follow-up reproduces the original R4 estimates and intervals within
5.4e-16. All cell-level outcomes and all three retention levels are included
in the result directories, not only these favorable aggregate contrasts.

## Continuous-estimator limit

At 50% retention, H has higher grid-mean fidelity than the globally optimized
fitting-label continuous-loss estimator, but lower fidelity than the optimized
estimator using all measurements. H minus the latter is -0.01195, -0.00897,
-0.01000, and -0.00949 in r0--r3, with all intervals below zero.
The full-record control uses the same total prepared-copy budget as the gate.
No general preference for discrete templates follows. Residual ranking is
also more selective than the tested combined ranking in stream averages;
the extra uncertainty conjunct is not generally justified by this grid.

The clock gives a consistent physical realization of the count model, with
an equivalent randomized measurement-setting likelihood. Neither the need
for a physical clock nor graph-spectral performance value is demonstrated.

## Complete records

- [Original R4](../biqmn/results/revision_experiments/R4_rate_matched/)
- [Margin follow-up](../biqmn/results/revision_experiments/R4_harm_sensitivity/)
- [R4 protocol](revision_r4_protocol.md)
- [Follow-up protocol](revision_r4_sensitivity_protocol.md)
- [Reproducibility and provenance](../REPRODUCIBILITY.md)

Main Figure 4 and SI Tables S17--S21 correspond to these records. Original
R3 inputs are preserved byte-for-byte as used by R4; see the release guide
for the correction of earlier Git newline normalization.
