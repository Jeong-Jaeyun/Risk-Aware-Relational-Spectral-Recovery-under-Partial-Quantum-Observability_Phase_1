import json

import numpy as np
import pytest

from biqmn.experiments.revision_identifiability import (
    AXES, METHODS, estimate, evaluate_job, legacy_weight, make_dataset, make_jobs,
    measurement_design, occupation_spectrum, qualify, stable_minimum,
)


def test_physical_constraints_and_negative_positive_controls():
    report = qualify(make_dataset())
    assert report["passed"], report
    assert report["maxima"]["constraint_residual"] < 1e-12
    json.dumps(report, allow_nan=False)


def test_data_split_and_grid_size_are_fixed():
    data = make_dataset()
    assert len(data["bank"]) == 32 and len(data["target_pairs"]) == 32
    assert data["max_test_reference_fidelity"] < 1-1e-12
    assert len(make_jobs()) == 1296


@pytest.mark.parametrize("code", ["bitflip", "phaseflip"])
def test_legacy_representation_loses_sign_but_occupation_preserves_it(code):
    z = np.linspace(-1, 1, 23)
    np.testing.assert_allclose(legacy_weight(z, code), legacy_weight(-z, code), atol=1e-14)
    np.testing.assert_allclose(occupation_spectrum(z).sum(axis=-1)/3-1, z, atol=1e-14)


def test_missing_all_counts_is_explicit_and_does_not_drop_targets():
    bank = np.array(make_dataset()["bank"])
    estimates, rank, indices = estimate(np.zeros(8), np.zeros(8), measurement_design(AXES["tilted"]), bank, "bitflip")
    assert rank == 0
    np.testing.assert_array_equal(estimates[:3], np.zeros((3, 3)))
    assert indices == {"raw": 0, "legacy": 0}
    assert stable_minimum([1., 1.+1e-15]) == 0


def test_replay_is_deterministic_budgeted_and_coupled_as_declared():
    dataset = make_dataset()
    job = {"key": "test", "code": "bitflip", "axis": "tilted", "copies": 128,
           "retained_labels": 4, "readout_flip": .05, "measurement_seed": 1}
    first, second = evaluate_job(job, dataset), evaluate_job(job, dataset)
    assert first == second
    fids = np.array(first["fidelities_by_pair_sign_method"])
    assert fids.shape == (32, 2, len(METHODS))
    np.testing.assert_allclose(fids[:, :, 0], fids[:, :, 1], atol=1e-12)
    np.testing.assert_allclose(fids[:, :, -1].mean(axis=1), .5, atol=1e-12)
    for record in first["measurement_records"]:
        assert sum(record["counts_all_labels"]) == 128
        assert sum(record["retained_mask"]) == 4
    equivalent_code = evaluate_job({**job, "code": "phaseflip"}, dataset)
    for a, b in zip(first["measurement_records"], equivalent_code["measurement_records"]):
        assert a["counts_all_labels"] == b["counts_all_labels"]
        assert a["successes_positive_target"] == b["successes_positive_target"]
