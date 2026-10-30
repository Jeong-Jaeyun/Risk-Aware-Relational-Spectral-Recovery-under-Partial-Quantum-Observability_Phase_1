# R4: switching-rate and continuous-estimator audit

Analysis rules frozen on 2026-10-29 after receipt of the second-round email,
before computing the R4 outcomes. This is a reviewer-prompted secondary analysis
of previously inspected R3 streams, not a preregistration or a new independent
replication. R3 source files and outputs remain unchanged.

## Questions

1. At equal expected switching rates, do the original H, U, and C3R gates
   select better proposals than uniform thinning of C2?
2. Over fixed retention levels, does residual ranking add selection information
   beyond uncertainty and fitting-score ranking?
3. How do the policies compare with optimized continuous estimators at the
   fitting-only and total measurement budgets?

## Data and counterfactual replay

Use all four authoritative R3 streams and all 24 cells per stream. Recover
the original count observations from their recorded RNG seeds. For every
record, verify counts, fit masks, fitting score, uncertainty, held-out residual,
candidate fidelities, and original gate decisions against the stored R3 output.
Fail the analysis on a discrepancy. No new test targets or count realizations
are generated. Bank, thresholds, and target pairs remain those of R3.

The physical Page-Wootters interpretation specifies a valid observation model;
it is not treated as a performance mechanism. R4 uses the resulting classical
count likelihood and does not assert a need for a physical clock in general
selective estimation.

## Primary comparison: original gates at common coverage

Within each cell and stream, keep the original C2 proposal, H, U, and C3R
decisions. C3R is their intersection. Let m be its number of accepted switches.
For each other policy with n accepted switches, retain each accepted switch
with probability m/n, independently of all outcomes. This represents a
randomized policy with exactly m expected switches. Integrate over this
thinning analytically rather than introducing a favorable random seed. Compare
conditional harmful fractions and total mean fidelity. Cells with m=0 contain
no information about conditional switch quality and must be reported as such.
Recompute m/n in every bootstrap resample.

## Secondary comparison: fixed retention curves

Within the original C2 proposal set, compare acceptance of fractions
q in {0.25, 0.50, 0.75}, fixed before the analysis. Rank proposals by:

- fitting score (C2 ranking control);
- uncertainty (U ranking);
- held-out residual (H ranking);
- max(u/t_u, h/t_h) (combined ranking), where the two positive denominators
  are the original stream-specific R3 calibration thresholds;
- uniform random retention (null control).

Lower scores are accepted first. The combined family rescales the two original
thresholds by a common factor and recovers the original conjunction at factor
one; these curves are not the original fixed-threshold policies. Round ranking
scores to 12 decimal places solely to preserve numerical ties. Randomize
uniformly within the boundary tie group to achieve exactly q times the number
of proposals in expectation. Integrate boundary randomization analytically.
No target fidelity is available to any ranking or cutoff. Batch score quantiles
use the test batch's observed diagnostic values but no outcomes; this is an
outcome-blind batch selection diagnostic, not a calibration-only deployment
rule. Report this distinction. Recalculate each batch cutoff in every bootstrap
resample.

## Optimized continuous controls

In addition to R3's radially projected least-squares A, compute the global
minimizer of the same weighted count loss over the Bloch ball:

    A*_fit = argmin_{||x|| <= 1} sum_fit n_k (d_k x - y_k)^2.

Solve the convex trust-region problem through the eigendecomposition of its
3 by 3 Gram matrix and a nonnegative Lagrange multiplier. Check feasibility,
KKT residual, and that its fitting loss does not exceed A's loss. Also fit
A*_all using all eight labels and the same total prepared-copy budget as the
gated policies. This addresses the opportunity cost of withholding counts.
The policies themselves remain unchanged; fidelity differences against these
controls are paired evaluator-only comparisons. Global optimization here is
of the specified count loss, not oracle target fidelity, and does not establish
optimality among all possible continuous estimators.

## Statistics and reporting

Use 5,000 paired two-way cluster bootstrap resamples of measurement seeds and
target pairs independently within each cell and stream, preserving the coupled
antipodal signs. Report pointwise 95% intervals, not simultaneous family-wise
intervals. Resample counts/rows, recompute coverage matching, and retain the
same resample for all policy differences. Calibration thresholds and banks
remain fixed. Stream summaries equally weight the 24 cells and resample the
shared seed/pair axes together across cells; code conventions are not counted
as independent replications. Never select only favorable cells.

Primary metrics are harmful fraction among accepted switches and overall mean
target fidelity, with paired differences against random thinning, U, A,
A*_fit, and A*_all. Also report unconditional harmful-switch rate and exact
expected switching rate. Descriptive q05 and exact lower-5%-mass CVaR use the
per-record outcome mixture, integrating thinning randomization; they differ
from R3's seed-averaged target-pair tail diagnostics. A nonzero mean gain is not
inferred solely from an interval for the harmful fraction.

Release all cell summaries, stream aggregates, replay/optimizer checks, source
and protocol hashes, and a machine-readable completion status. No performance
claim is made from the veto-subset inequality alone. Additional simulations
will be designed separately if the resulting comparisons leave an answerable
scientific question unresolved; any such work will have its own protocol.
