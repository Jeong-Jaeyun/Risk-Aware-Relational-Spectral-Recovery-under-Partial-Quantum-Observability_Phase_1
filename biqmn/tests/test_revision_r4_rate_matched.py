import numpy as np
from scipy.optimize import minimize

from biqmn.experiments.revision_r4_rate_matched import constrained_wls, ranked_probabilities, ranked_totals


def test_constrained_wls_matches_independent_constrained_solver():
    rng = np.random.default_rng(12)
    for _ in range(12):
        design = rng.normal(size=(8, 3))
        means = rng.normal(size=8)
        weights = rng.integers(1, 50, size=8)
        result, kkt = constrained_wls(means, weights, design)
        objective = lambda x: np.sum(weights * (design @ x - means) ** 2)
        independent = minimize(objective, np.zeros(3), constraints=[{'type': 'ineq', 'fun': lambda x: 1-x@x}],
                               method='SLSQP', options={'ftol': 1e-10, 'maxiter': 1000})
        assert np.linalg.norm(result) <= 1 + 1e-9
        assert kkt < 1e-8
        assert abs(objective(result) - independent.fun) < 1e-5


def test_ranked_matching_integrates_ties_and_recomputes_bootstrap_cutoff():
    scores = np.array([1., 1., 2., 3., 9.])
    proposed = np.array([True, True, True, True, False])
    probability = ranked_probabilities(scores, proposed, .25)
    np.testing.assert_allclose(probability, [.5, .5, 0, 0, 0])
    weights = np.array([[1., 1., 1., 1., 1.], [2., 0., 0., 2., 1.]])
    delta = np.array([.1, -.2, .4, -.5, 99.])
    harmful = (delta < 0).astype(float)
    mass, gain, bad = ranked_totals(scores, proposed, .5, weights, delta, harmful)
    np.testing.assert_allclose(mass, [2, 2])
    np.testing.assert_allclose(gain, [-.1, .2])
    np.testing.assert_allclose(bad, [1, 0])
