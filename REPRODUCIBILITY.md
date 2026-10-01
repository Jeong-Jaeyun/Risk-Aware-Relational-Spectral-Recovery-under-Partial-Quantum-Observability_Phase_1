# Reproducibility guide

This release separates the evidentiary roles of the revision experiments.

- **R3 is the primary result.** It evaluates a corrected held-out residual gate:
  the continuous candidate and direct nearest-template candidate are fit on
  fitting labels and scored unchanged on complementary validation labels.
- **R1 is a physical construction qualification.** It verifies the finite-clock
  setup but is not a recovery-efficacy experiment.
- **R2 is archival only.** It is retained because its comparison refit the
  continuous candidate on validation labels and is therefore superseded by R3.
- **The submitted grid is an audit artifact.** It documents the degenerate-clock
  and uncertainty-gate findings; it is not efficacy evidence.

## Environment

The maintained environment is the `quantum` conda environment. From `biqmn/`:

```powershell
conda run -n quantum --no-capture-output pytest -q `
  tests/test_revision_r3_holdout_recovery.py `
  tests/test_revision_identifiability.py `
  tests/test_revision_r2_recovery.py
```

## Re-running R3

The frozen design is in
[`manuscript/revision_r3_protocol.md`](manuscript/revision_r3_protocol.md).
The runner refuses to overwrite output directories.

```powershell
cd biqmn
conda run -n quantum --no-capture-output python -m biqmn.experiments.revision_r3_holdout_recovery `
  --replication 0 --workers 6 `
  --output results/revision_experiments/R3_reproduction_r0
```

Repeat with `--replication 1`, `2`, and `3`, using a distinct output path for
each independent stream family. Each full run records the frozen data split,
calibration thresholds, raw records, two-way bootstrap summaries, and
source/protocol SHA-256 values.

## Released result artifacts

The authoritative artifacts are:

- `biqmn/results/revision_experiments/R1_full/`
- `biqmn/results/revision_experiments/R2_full/` (archival)
- `biqmn/results/revision_experiments/R3_corrected_r0/`
- `biqmn/results/revision_experiments/R3_independent_r1/`
- `biqmn/results/revision_experiments/R3_independent_r2/`
- `biqmn/results/revision_experiments/R3_independent_r3/`
- `biqmn/results/revision_audit/submitted_seed10/`

The four R3 `results.json` files have SHA-256 values listed in
[`manuscript/revision_r3_results.md`](manuscript/revision_r3_results.md).

## Non-release material

Scratch outputs, superseded runs, generated TeX auxiliary files, local IDE
settings, design drafts, and locally stored reference PDFs are intentionally
excluded from the submission branch.
