# R4 follow-up: harm-margin sensitivity and paired fidelity

Rules fixed on 2026-10-29 after inspecting the original R4 findings and before
calculating this follow-up. This is a further reviewer/author-prompted secondary
analysis of the same four R3 streams, not a new independent replication or a
preregistered confirmatory experiment. Preserve the original R3/R4 files.

Use every original stream and cell, the original C2 proposal set and calibration
thresholds, and the original fixed/common-coverage and 25/50/75% batch-ranking
rules. Do not retune a policy or ranking on a harm label. Classify a switch as
harmful when F_B < F_A - epsilon for all epsilon in
{1e-12, 0.001, 0.005, 0.01}. Epsilon=1e-12 reproduces the original numerical
tolerance; the positive margins are descriptive sensitivity choices in absolute
fidelity units, not application-validated utility thresholds. The 0.01 margin
matches the size of the historical audit tolerance but does not identify the
historical experiment with R3/R4.

Reuse the 5,000 paired two-way seed/target-pair bootstrap draws of R4 exactly
(RNG seed 2026102900 + stream). Recompute matching factors and batch cutoffs in
each resample, integrate random thinning and boundary ties analytically, and
equally average cells. Original fixed-gate conditional harm uses the twelve
positive-coverage cells; the ranking summaries use all 24 cells. Report
pointwise conditional intervals and preserve the deployment-versus-batch
distinction. Report all declared margins and retention fractions, including
unfavorable or inconclusive contrasts. Mean-fidelity calculations use the full
signed F_B-F_A and do not discard losses within the harm margin.

The main sensitivity presentation is H-minus-U conditional harmful fraction at
50% retention, with all four margins, in each of four streams. Also release
all-cell, all-policy results for the original fixed gates and all three ranking
retention levels. Direct paired H-minus-U overall mean-fidelity differences
are reported at all three retention levels. These are expected policy outcomes
under the batch ranking/randomization rule, not a claim for a calibrated
deployment policy.

Verify the epsilon=1e-12 results and all mean-fidelity estimates/intervals against
the saved R4 summaries. Verify the archived raw inputs and frozen R4 source and
protocol hashes. Release this protocol, analysis source, complete outputs, and
completion metadata in the updated reproducibility archive. No new count
realizations, targets, or optimized estimators are needed for these contrasts.
