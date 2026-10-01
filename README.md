# Risk-Aware Template-Switching Control under Partial Quantum Observability

This repository contains the manuscript, supplementary information, reference notes,
and the `biqmn` Python code used for the submitted-grid audit and the revised
finite-data template-switching experiments.

The revised positive result is R3: a corrected held-out residual gate that fits
both a continuous candidate and a direct nearest-template candidate on fitting
records, then scores the unchanged candidates on complementary validation
records. It is a finite-copy safety-filter experiment, not evidence for a
spectral-representation advantage or a QEC decoder. The submitted C3R grid is
retained as an auditable historical artifact and is not final efficacy evidence.

## Repository Layout

```text
biqmn/                  Python package, configs, tests, and result files
legacy/                 recoverable superseded workspace snapshots
design/                 theory notes and earlier design drafts
manuscript/             main text, SI, frozen protocols, response, and tables
reference/              curated papers and citation/reference notes
LetsDoThis.md           working notes for manuscript revisions
```

## Code Quick Start

The maintained revision environment is the `quantum` conda environment.

```powershell
cd biqmn
conda activate quantum
python -m pip install -e ".[dev]"
python -m pytest
```

The historical submitted-grid C3R reproduction script is:

```powershell
.\scripts\run_c3r_seed10.ps1
```

It runs the five historical C3R regime experiments with the default ten-seed set
`11,12,13,14,15,16,17,18,19,20` and writes outputs under `biqmn/results/`.

To rebuild derived C3R tables from the existing raw JSON rows without rerunning
the simulations:

```powershell
.\scripts\rebuild_c3r_results.ps1
```

See [biqmn/README.md](biqmn/README.md) for the full code and result
reproducibility guide. The frozen R3 protocol is
[manuscript/revision_r3_protocol.md](manuscript/revision_r3_protocol.md), and
its concise result summary is
[manuscript/revision_r3_results.md](manuscript/revision_r3_results.md).
The release scope and exact artifact roles are stated in
[REPRODUCIBILITY.md](REPRODUCIBILITY.md).

## R3 reproduction

R3 never overwrites an existing output directory. From `biqmn/`, a fresh
replication-0 rerun is:

```powershell
conda run -n quantum --no-capture-output python -m biqmn.experiments.revision_r3_holdout_recovery `
  --replication 0 --workers 6 `
  --output results/revision_experiments/R3_reproduction_r0
```

Use `--replication 1`, `2`, and `3` with distinct output directories for the
independent stream families. The four authoritative runs are
`R3_corrected_r0`, `R3_independent_r1`, `R3_independent_r2`, and
`R3_independent_r3` under `biqmn/results/revision_experiments/`; each includes
the frozen dataset, thresholds, raw records, two-way bootstrap summary, report,
and source/protocol manifest.

## Manuscript Build

The active main manuscript source is:

```text
manuscript/ioplatextemplate/iopjournal-template-revised_3.tex
```

The active SI source is `manuscript/supplementary-file.tex`. A LaTeX engine is
required to build the final PDFs; it is not bundled with this repository.
