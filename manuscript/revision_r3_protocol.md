# R3: corrected held-out residual gate and independent replications

Date frozen: 2026-09-30, before any R3 simulation is run.  This is a
repository-frozen protocol, not an externally registered preregistration.  R2
is retained unchanged because its output manifest hashes its prior source and
protocol.

## Purpose and claim boundary

R3 corrects a definition issue identified during the R2 audit.  In R2, the
validation residual of the discrete template was compared with a continuous
estimate refit on the validation labels.  R3 instead fits both candidates on
the fitting labels and scores both unchanged candidates on the complementary
validation labels.  The resulting gate is called a **held-out residual gate**.
It is not called relational-spectral admissibility and is not a claim of a
spectral-representation advantage.

The question is operational: can an out-of-fit-label residual test reduce the
risk of accepting a discrete template in place of a continuous estimate, without
using the hidden target state?  R3 is a multi-copy state-restoration decision
study under a known engineered finite-clock model.  It is not a generic QEC
channel, an unknown-state recovery experiment, or an entanglement-fidelity
benchmark.

## Data-generating model

The physical model is the qualified R1 model.  A logical qubit is encoded in a
three-qubit bit-flip or phase-flip repetition code.  The finite clock has eight
nonorthogonal POVM labels and a tilted known logical Hamiltonian.  Independent
code-matched physical Pauli noise is applied before finite-shot logical
population measurements, followed by the declared binary readout flip.

The primary grid is code {bitflip, phaseflip}, prepared copies {256, 1024},
physical-noise probability {0.01, 0.05, 0.10}, readout-flip probability
{0, 0.05}, and 12 measurement seeds.  Each cell has 64 held-out target states
arranged as 32 antipodal pairs.  The two code conventions are coupled
basis-equivalent checks, not independent replications.

R3 runs replicate 0, which reuses R2's fixed bank/calibration/test RNG streams
only to isolate the gate-definition correction, plus independent replications
1, 2, and 3.  Each independent replication uses disjoint bank, calibration,
test-target, and measurement RNG streams.  No test target is in its bank or
calibration set.

## Candidates and policies

For each record, four clock labels are randomly selected as fitting labels and
the remaining four are validation labels.  The split and count record are shared
by every candidate and policy.

- **A (continuous):** Bloch-ball projected weighted least-squares estimate fit
  on fitting-label counts.
- **B (direct nearest template):** nearest fixed bank element under the same
  fitting-label weighted loss.  This is the direct observation-space
  nearest-template baseline; no graph or spectral representation is used.
- **C2:** score-only proposal to substitute B for A.
- **U:** C2 plus the uncertainty threshold.
- **H:** C2 plus the held-out residual threshold.
- **C3R:** C2 plus both the uncertainty and held-out residual thresholds.

Let `L_val(x)` be the weighted squared loss of an unchanged candidate `x` on
the validation-label counts.  R3 defines

`h = L_val(B_fit) - L_val(A_fit)`.

Neither candidate is refit on validation labels.  All three thresholds (score,
uncertainty, and h) are the 75th empirical quantiles calculated once from a
separate calibration set at the fixed bit-flip, 1,024-copy, physical-noise 0.05,
readout-flip 0.05 operating point.  The thresholds are then fixed across every
held-out grid cell and replication.

The hidden target vector is used only after policy decisions to calculate
fidelity.  An oracle nearest-template fidelity is additionally reported as an
offline bank-resolution diagnostic; it is never a policy input.

## Statistics and interpretation

For each policy, R3 reports mean fidelity, q05, exact-mass CVaR(5%), switch
rate, harmful-switch (false-safe) rate, and paired policy differences.  The
primary intervals are 95% two-way cluster bootstrap intervals that resample both
the 32 target pairs and the 12 measurement seeds.  They therefore describe
finite-target and finite-measurement variation conditional on the fixed model,
grid, and calibration set; they do not include calibration-threshold uncertainty.

The principal comparison is H minus C2 false-safe rate.  The combined-gate
comparison C3R minus U is reported separately.  A lower harmful-switch rate is
not sufficient for a recovery-performance claim: every report must also show the
mean-fidelity difference versus A.  Results are described as finite-data
template-switch safety only when their scope and the continuous-estimator limit
are stated together.
