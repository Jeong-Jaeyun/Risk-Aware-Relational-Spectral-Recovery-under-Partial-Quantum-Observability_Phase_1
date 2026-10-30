import numpy as np

from biqmn.experiments.revision_r4_harm_sensitivity import harm_labels, ranked_outcomes


def test_positive_margins_exclude_small_losses_and_preserve_large_losses():
    a = np.ones(3)
    b = np.array([.98,.995,.999999])
    labels = harm_labels(a,b)
    np.testing.assert_array_equal(labels[:,0],[1,1,1])
    np.testing.assert_array_equal(labels[:,-1],[1,0,0])
    assert np.all(np.diff(labels,axis=1)<=0)


def test_vectorized_ranked_outcomes_matches_explicit_resampled_tie_selection():
    score = np.array([1.,1.,2.,3.])
    proposed = np.ones(4,dtype=bool)
    weights = np.array([[1.,1.,1.,1.],[2.,0.,0.,2.]])
    outcomes = np.array([[.1,0.,0.],[-.02,1.,1.],[.3,0.,0.],[-.005,1.,0.]])
    mass,totals = ranked_outcomes(score,proposed,.5,weights,outcomes)
    np.testing.assert_allclose(mass,[2,2])
    np.testing.assert_allclose(totals,[outcomes[0]+outcomes[1],2*outcomes[0]])
