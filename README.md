# Background-Independent Relational Spectral Recovery

This repository contains the manuscript, supplementary information, reference notes,
and the `biqmn` Python code used for the reported relational spectral recovery
experiments in partially observable qubit-network/QEC settings.

The reproducibility package is centered on `biqmn/`. That directory contains the
installable Python package, YAML experiment configurations, tests, reproduction
scripts, and the C3R result files used by the manuscript.

## Repository Layout

```text
biqmn/                  Python package, configs, tests, and result files
design/                 theory notes and earlier design drafts
manuscript/             main text, supplementary information, figures, and tables
reference/              curated papers and citation/reference notes
LetsDoThis.md           working notes for manuscript revisions
```

## Code Quick Start

The experiments were run in the `QEC` conda environment.

```powershell
cd biqmn
conda activate QEC
python -m pip install -e ".[dev]"
python -m pytest
```

The full C3R reproduction script is:

```powershell
.\scripts\run_c3r_seed10.ps1
```

It runs the five reported C3R regime experiments with the default ten-seed set
`11,12,13,14,15,16,17,18,19,20` and writes outputs under `biqmn/results/`.

To rebuild derived C3R tables from the existing raw JSON rows without rerunning
the simulations:

```powershell
.\scripts\rebuild_c3r_results.ps1
```

See [biqmn/README.md](biqmn/README.md) for the full code and result
reproducibility guide.

## Manuscript Build

The active main manuscript source is:

```text
manuscript/main/quantum-template.tex
```

The active supplementary source is:

```text
manuscript/supplementary-file.tex
```

Both files were compiled with `pdflatex` during manuscript preparation.
