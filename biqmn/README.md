# biqmn: finite-data template-switching evidence

The maintained release contains the observation-model core, R1/R2/R3 runners,
and the R4 equal-coverage and harm-sensitivity analyses. Older submitted-grid
simulators are historical material in Git history; they are not required to
reproduce the current R4 results.

Install dependencies in the maintained quantum environment from this folder:

~~~powershell
conda activate quantum
python -m pip install -e ".[dev]"
python -m pytest -q
~~~

The authoritative R3 inputs and both complete R4 result directories are in
results/revision_experiments/. Never overwrite these directories. For fresh
R4 analyses:

~~~powershell
python -m biqmn.experiments.revision_r4_rate_matched --workers 4 --output results/revision_experiments/R4_reproduction
python -m biqmn.experiments.revision_r4_harm_sensitivity --workers 4 --output results/revision_experiments/R4_sensitivity_reproduction
~~~

No new count realizations are needed. The second command retains all policy
decisions while varying the evaluator's absolute harm margin. It also verifies
the original R4 estimates and intervals. The evidence remains a secondary
batch-selection analysis, with pointwise conditional intervals and a known
full-record continuous-estimator limit.

See [the release guide](../REPRODUCIBILITY.md) for exact provenance,
environment versions, R3 reproduction, figure/table generation, and metric
clarifications. From the repository root, verify all frozen released files:

~~~powershell
python biqmn/scripts/verify_release.py
~~~
