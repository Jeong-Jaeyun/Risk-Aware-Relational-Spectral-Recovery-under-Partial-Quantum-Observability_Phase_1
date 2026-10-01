import numpy as np

from biqmn.experiments.revision_identifiability import AXES
from biqmn.experiments.revision_r2_recovery import (
    POLICIES,
    _draw_record,
    calibrate,
    evaluate_job,
    make_dataset,
    physical_measurement_design,
)


def test_r2_uses_disjoint_bank_calibration_and_test_targets():
    dataset = make_dataset()
    bank = np.asarray(dataset["bank"])
    test = np.asarray(dataset["test_pairs"]).reshape(-1, 3)
    calibration = np.asarray(dataset["calibration_pairs"]).reshape(-1, 3)
    assert np.max((1 + test @ bank.T) / 2) < 1 - 1e-12
    assert np.max((1 + test @ calibration.T) / 2) < 1 - 1e-12


def test_r2_observation_record_couples_antipodes_without_gate_access_to_target():
    dataset = make_dataset()
    design = physical_measurement_design("bitflip", AXES["tilted"], 0.05)
    thresholds = calibrate(dataset)
    rows = _draw_record(np.asarray(dataset["test_pairs"])[0, 0], np.random.default_rng(7), design,
                        np.asarray(dataset["bank"]), 256, 0.05, thresholds)
    assert design.shape == (8, 3)
    assert np.linalg.matrix_rank(design) == 3
    assert rows[0]["counts"] == rows[1]["counts"]
    assert rows[0]["fit_mask"] == rows[1]["fit_mask"]
    assert set(rows[0]["decision"]) == {"c2_score", "u_uncertainty", "s_structural", "c3r",
                                          "proposal", "uncertainty_ok", "structural_ok"}
    assert all(0 <= row["fidelity_a"] <= 1 and 0 <= row["fidelity_b"] <= 1 for row in rows)


def test_r2_job_emits_every_declared_policy():
    dataset = make_dataset()
    thresholds = calibrate(dataset)
    result = evaluate_job({"code": "phaseflip", "axis": "tilted", "copies": 256,
                           "physical_noise": 0.01, "readout_flip": 0.0, "measurement_seed": 0},
                          dataset, thresholds)
    assert result["design_rank"] == 3
    assert len(result["records"]) == 64
    assert set(result["records"][0]["decision"]).issuperset(set(POLICIES[2:]))
