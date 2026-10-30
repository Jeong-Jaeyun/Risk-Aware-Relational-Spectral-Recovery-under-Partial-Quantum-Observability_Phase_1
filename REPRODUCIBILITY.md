# Reproducibility and provenance

## Evidentiary scope

R4 tests selection quality at equal **expected** switching rates and compares
the policies with globally optimized continuous-loss estimators. Its separate
harm-margin follow-up changes evaluator labels, not policy decisions. Both
reuse previously inspected R3 streams. The batch rankings use observed
diagnostics without target outcomes; they are not calibration-only deployment
rules. Intervals are pointwise and conditional on the fixed bank, calibration,
model, and grid.

R1 qualifies the finite-clock construction. R2 is superseded. R3's nested-veto
unconditional harmful-rate reduction alone is insufficient to establish useful
selection. Full-record continuous estimation retains its mean-fidelity
advantage. No general quantum-recovery or spectral-performance advantage is
claimed.

## Authoritative artifacts

Under biqmn/results/revision_experiments/:

- R1_full/: construction qualification.
- R2_full/: superseded preliminary gate, archival.
- R3_corrected_r0/, R3_independent_r1/, R3_independent_r2/,
  R3_independent_r3/: four original count-record streams.
- R4_rate_matched/: all 96 cell-stream combinations, continuous controls,
  fixed-gate common coverage, and 25/50/75% batch rankings.
- R4_harm_sensitivity/: every cell, policy, and declared margin; direct
  paired H-minus-U mean-fidelity comparisons.

Each R4 directory includes a manifest, stream summaries, complete summary,
report, and successful completion status. These outputs and the four R3 input
directories are released directly as files, rather than only inside a ZIP.

## Hash preservation

RELEASE_MANIFEST.json records SHA-256 values of the released evidence,
protocols, analysis sources, manuscript, and figure assets. Run
python biqmn/scripts/verify_release.py after cloning.

The earlier Git release normalized the R3 JSON files from CRLF to LF. The
numeric contents were unchanged, but the file hashes differed from the exact
Windows-generated inputs used by R4. This release restores the original
input bytes and disables Git text conversion for result artifacts. The R4
input hashes therefore match the released R3 files on all platforms.
The verifier checks this correspondence. This is a provenance correction,
not a change to a simulated observation or reported result.

The R3 manifests hash the original protocol at commit
9354f1fd652cc5b63d2a9ffaa8289f260a8dd7a6:
90c2941f4f1a7a64a7c8a40fc2c50141d6132aee1b4767d5bb32fefe9f6a1644.
That version is retained at
manuscript/protocol_archive/revision_r3_protocol_frozen_9354f1f.md.
The current manuscript/revision_r3_protocol.md includes the documented
post-run threshold-wording clarification, without changing the design.
The original R4 and follow-up source/protocol hashes are checked separately.

## Environment and validation

The runs used Python 3.12, NumPy 2.5.0, and SciPy 1.18.0 in the quantum
conda environment. Qiskit, Qiskit Aer, PyYAML, and Matplotlib are declared in
biqmn/pyproject.toml. From biqmn/:

~~~powershell
conda run -n quantum --no-capture-output python -m pytest -q
~~~

The unit tests include independent constrained-optimizer checks, exact
expected-mass matching with numerical ties, harm-margin behavior, and the
R1/R2/R3 observation design. The sensitivity runner also reproduces the
original R4 point estimates and intervals and checks archived input hashes.

## R4 and sensitivity reproduction

From biqmn/, using fresh output directories:

~~~powershell
conda run -n quantum --no-capture-output python -m biqmn.experiments.revision_r4_rate_matched --workers 4 --output results/revision_experiments/R4_reproduction
conda run -n quantum --no-capture-output python -m biqmn.experiments.revision_r4_harm_sensitivity --workers 4 --output results/revision_experiments/R4_sensitivity_reproduction
~~~

The sensitivity runner verifies the authoritative original R4 outputs; it
does not overwrite them. Both runners use the released original R3 inputs.
Allow up to six workers; four stream workers are used in the authoritative
R4 runs. Threaded BLAS can be limited to one thread per worker as needed.

## R3 reproduction

From biqmn/:

~~~powershell
conda run -n quantum --no-capture-output python -m biqmn.experiments.revision_r3_holdout_recovery --replication 0 --workers 6 --output results/revision_experiments/R3_reproduction_r0
~~~

Repeat with replications 1--3 and distinct output directories. Replication 0
reuses R2's streams only to isolate the gate correction. The code conventions
are coupled checks, not independent replications.

## Tables, figures, and manuscript

The presentation modules regenerate the released figure and SI tables from
the authoritative summaries:

~~~powershell
python -m biqmn.experiments.revision_r4_presentation
python -m biqmn.experiments.revision_r4_sensitivity_presentation
~~~

The main source is manuscript/ioplatextemplate/iopjournal-template-revised_3.tex;
the SI is manuscript/supplementary-file.tex. Compile them from their own
directories using latexmk -pdf. The local numerical bibliography style prints
article titles and DOI links. The ORCID icon and generated R4 assets are included.

## Metric clarification

The archived R3 field cvar05_exact_mass averages the lowest two of 32
seed-averaged target-pair fidelities, i.e. 6.25% mass. It is not an exact
fractional 5% tail. The manuscript's R4 selection and mean-fidelity contrasts
do not use that field. R4's per-record tail summaries integrate the exact
lower 5% outcome mass, including fractional boundary weights.
