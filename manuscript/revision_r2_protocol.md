# R2: held-out finite-clock template-switching risk test

## Purpose and claim boundary

R2 is a pre-registered **multi-copy restoration/decision** experiment built on
the physically qualified finite-clock model in R1.  It is not an unknown-state
QEC-channel or entanglement-fidelity experiment, and it cannot establish an
advantage merely from representing an observation by a spectrum.

The narrow question is whether a structural compatibility check has an effect
separate from an uncertainty threshold when a controller considers switching
from a continuous estimate to a discrete reference-template estimate.  The
study reports a negative result and narrows the manuscript claim if that effect
is absent.

## Data-generating model

R2 uses the R1 zero-energy clock--logical-system construction, its eight
nonorthogonal clock POVM labels, and the tilted logical Hamiltonian.  The
logical qubit is encoded into the three-qubit bit-flip or phase-flip repetition
code.  After each conditional slice is prepared, independent code-matched
physical Pauli noise is applied before measurement.  Measurement records are
finite-shot logical-population observations with the declared binary readout
flip probability.

The reference-template bank, calibration targets, and test targets are
generated from distinct fixed RNG streams.  No test target is in the bank or
the calibration set.  The controller receives only label-indexed count data,
the known Hamiltonian, and the fixed bank; target density matrices are reserved
for evaluation.

## Candidate and policy comparison

For each target, four clock labels form a fitting split and the complementary
four form a validation split.  The split is sampled once per measurement seed
and shared by every candidate and policy.

- **A (continuous):** physical, Bloch-ball projected weighted least-squares
  estimate from fitting-label counts.
- **B (template):** nearest fixed reference-template trajectory under the same
  fitting-label weighted loss.
- **C2:** score-only proposal to substitute B for A.
- **U:** C2 plus an uncertainty threshold only.
- **S:** C2 plus a structural compatibility threshold only; compatibility is
  the candidate's validation-label prediction residual relative to A.
- **C3R:** C2 plus both U and S.

Score, uncertainty, and structural thresholds are calibrated exclusively on
the separate calibration targets at the middle shot/noise operating point.
They are then fixed for every held-out test cell.  The structural residual is
an out-of-fit-split prediction check; it is not target fidelity and is not
tuned on test outcomes.

An invertible signed-occupation spectrum may be recorded as a positive
representation check, but it must reproduce the raw population estimator.  No
performance difference between those equal-information representations is
claimed.

## Grid and statistics

The primary grid is: code {bitflip, phaseflip}; prepared copies {256, 1024};
physical noise {0.01, 0.05, 0.10}; readout flip {0, 0.05}; and 12 independent
measurement seeds.  Each cell evaluates 64 held-out target states arranged as
32 antipodal pairs.  The two code conventions are coupled basis-equivalent
checks rather than independent replications.

Reported outcomes are mean target fidelity, q05 fidelity, exact-mass CVaR(5%),
false-safe switch rate (a switch worse than A), proposed/safe/harmful switch
counts, and the structural-only/uncertainty-only block rates.  Confidence
intervals use paired bootstrap resampling of target pairs after averaging
measurement seeds; policy comparisons share every count record.

## Falsification rule

R2 supports a distinct structural gate only if S has a nonzero, pre-specified
block rate and reduces false-safe switches relative to C2 after accounting for
the uncertainty-only policy U.  If S never blocks, or its apparent benefit is
fully reproduced by U, the manuscript will describe the controller as
uncertainty-threshold safety control with template candidate generation, not a
relational-spectral admissibility contribution.

Regardless of outcome, R2 is described as finite-copy state-restoration
decision-making under a known engineered model, not generic QEC of a single
unknown state.
