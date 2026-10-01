# R3 results: corrected held-out residual template-switching test

R3 corrects the R2 validation definition.  Both the continuous candidate A and
the direct nearest-template candidate B are fitted on the fitting labels, then
scored unchanged on the complementary validation labels.  The gate statistic is
the difference between their validation losses.  R3 is a finite-copy
template-switch decision experiment, not a spectral-representation or QEC
decoder benchmark.

The full results are stored in:

- `biqmn/results/revision_experiments/R3_corrected_r0/`
- `biqmn/results/revision_experiments/R3_independent_r1/`
- `biqmn/results/revision_experiments/R3_independent_r2/`
- `biqmn/results/revision_experiments/R3_independent_r3/`

Each run contains 24 grid cells, 12 measurement seeds per cell, 32 antipodal
target pairs, two-way target-pair/measurement-seed bootstrap intervals, and a
source/protocol manifest.  Replication 0 uses R2's RNG streams to isolate the
gate-definition correction.  Replications 1--3 use disjoint bank, calibration,
target, and measurement streams.

| R3 stream | H minus C2 false-safe CI negative | C3R minus U false-safe CI negative | Cells with positive C3R minus A mean-fidelity estimate | Grid mean C3R minus A fidelity |
|---|---:|---:|---:|---:|
| corrected r0 | 24/24 | 12/24 | 0/24 | -0.001184 |
| independent r1 | 24/24 | 8/24 | 2/24 | -0.000550 |
| independent r2 | 24/24 | 12/24 | 12/24 | +0.001251 |
| independent r3 | 24/24 | 6/24 | 6/24 | -0.000011 |

At the fixed middle grid point (bit-flip, 1,024 copies, physical noise 0.05,
readout flip 0.05), the H minus C2 false-safe differences are -14.844,
-8.333, -10.677, and -5.990 percentage points in streams r0--r3; every two-way
95% interval excludes zero.  The C3R minus U values are -7.813, -3.125,
-6.771, and -1.823 percentage points, respectively, also with intervals below
zero at that one point.

The supported claim is therefore limited to safety filtering of a discrete
template proposal by a held-out residual check.  The results do not establish a
consistent mean-fidelity advantage over A, an advantage of a spectral
representation, or QEC-channel recovery efficacy.
