# Risk-Aware Template-Switching Control under Partial Quantum Observability

This repository releases the manuscript, simulation inputs, and analyses for
a finite-copy template-switching decision study. The current evidence is R4
and its harm-margin follow-up, using the four existing R3 streams.

At equal expected switching rates, a held-out residual contains information
about harmful template proposals beyond random thinning and uncertainty
ranking in this testbed. The result persists at an absolute fidelity-loss
margin of 0.01. Full-record optimized continuous estimation nevertheless has
higher grid-mean fidelity than the tested switching rankings. These are
secondary batch-selection analyses, not new independent replications or
calibration-only deployment policies. They establish no clock-specific,
graph-spectral, or QEC-decoder advantage.

## Evidence and files

| Record | Role |
|---|---|
| R1 | Physical consistency and observability qualification |
| R2 | Superseded preliminary gate; archival only |
| R3 | Four finite-shot streams and nested fixed-gate comparisons |
| R4 | Equal-coverage comparisons and optimized continuous controls |
| R4 harm sensitivity | Fixed decisions at margins 1e-12, 0.001, 0.005, 0.01; direct paired H-minus-U fidelity |

- [Results and limits](manuscript/revision_r4_results.md)
- [Reproduction and provenance](REPRODUCIBILITY.md)
- [R4 protocol](manuscript/revision_r4_protocol.md) and
  [follow-up protocol](manuscript/revision_r4_sensitivity_protocol.md)
- [Complete result directories](biqmn/results/revision_experiments/)
- [Main source](manuscript/ioplatextemplate/iopjournal-template-revised_3.tex),
  [main PDF](manuscript/ioplatextemplate/iopjournal-template-revised_3.pdf),
  [SI source](manuscript/supplementary-file.tex), and
  [SI PDF](manuscript/supplementary-file.pdf)
- [Byte-level release inventory](RELEASE_MANIFEST.json)

Private reviews, response letters, submission bundles, scratch files, IDE
state, and LaTeX intermediates are not part of this public release. The
submitted-grid audit remains historical material; it is not the evidence
for R4's selection-quality findings.

## Reproduce

The maintained environment is Python 3.12 in the quantum conda environment.
Dependencies are declared in biqmn/pyproject.toml; authoritative run manifests
record the versions used. From biqmn/:

~~~powershell
conda run -n quantum --no-capture-output python -m pytest -q
conda run -n quantum --no-capture-output python -m biqmn.experiments.revision_r4_rate_matched --workers 4 --output results/revision_experiments/R4_reproduction
conda run -n quantum --no-capture-output python -m biqmn.experiments.revision_r4_harm_sensitivity --workers 4 --output results/revision_experiments/R4_sensitivity_reproduction
~~~

Use fresh output directories: runners refuse to overwrite existing runs.
The four R3 datasets and thresholds are included, so R4 requires no new count
realizations. See the reproducibility guide for rebuilding R3 itself.

Verify the frozen files from the repository root:

~~~powershell
python biqmn/scripts/verify_release.py
~~~

Compile the main LaTeX source from manuscript/ioplatextemplate/ and the SI
from manuscript/, using latexmk -pdf. Required figures, the ORCID icon,
and the local bibliography style are included.
