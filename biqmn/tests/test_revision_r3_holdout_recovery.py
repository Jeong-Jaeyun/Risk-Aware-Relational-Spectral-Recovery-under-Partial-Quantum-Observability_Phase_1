from unittest.mock import patch

import numpy as np

from biqmn.experiments import revision_r2_recovery as r2
from biqmn.experiments.revision_identifiability import AXES
from biqmn.experiments.revision_r3_holdout_recovery import (
    POLICIES,
    _draw_record,
    calibrate,
    evaluate_job,
    make_dataset,
    summarize,
)


def test_r3_replications_have_disjoint_bank_calibration_and_test_targets():
    for replication in range(4):
        dataset = make_dataset(replication)
        bank = np.asarray(dataset["bank"])
        calibration = np.asarray(dataset["calibration_pairs"]).reshape(-1, 3)
        test = np.asarray(dataset["test_pairs"]).reshape(-1, 3)
        assert np.max((1 + test @ bank.T) / 2) < 1 - 1e-12
        assert np.max((1 + test @ calibration.T) / 2) < 1 - 1e-12


def test_r3_scores_the_fitting_candidates_without_validation_refit():
    dataset = make_dataset(0)
    design = r2.physical_measurement_design("bitflip", AXES["tilted"], 0.05)
    with patch.object(r2, "_fit", wraps=r2._fit) as fitted:
        rows = _draw_record(
            np.asarray(dataset["test_pairs"])[0, 0],
            np.random.default_rng(7),
            design,
            np.asarray(dataset["bank"]),
            1024,
            0.05,
            None,
        )
    assert fitted.call_count == 2
    assert len(rows) == 2
    assert all(row["validation_loss_a_fit"] >= 0 for row in rows)
    assert all(row["validation_loss_b_fit"] >= 0 for row in rows)


def test_r3_job_and_summary_use_declared_policies_and_two_way_intervals():
    dataset = make_dataset(1)
    thresholds = calibrate(dataset)
    result = evaluate_job({
        "code": "phaseflip",
        "axis": "tilted",
        "copies": 256,
        "physical_noise": 0.01,
        "readout_flip": 0.0,
        "measurement_seed": 0,
    }, dataset, thresholds)
    assert result["design_rank"] == 3
    assert len(result["records"]) == 64
    assert set(result["records"][0]["decision"]).issuperset(set(POLICIES[2:]))
    summary = summarize([result], pilot=True)
    assert summary[0]["bootstrap"]["method"].startswith("two_way")
    assert "ci95_two_way" in summary[0]["policies"]["c3r"]
