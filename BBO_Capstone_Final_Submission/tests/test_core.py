import numpy as np

from bbo_capstone.data import load_datasets
from bbo_capstone.experiment import propose_query, run_experiment
from bbo_capstone.surrogate import GaussianProcessSurrogate, expected_improvement, posterior_variance, ucb


def test_loads_eight_documented_functions() -> None:
    datasets = load_datasets()
    assert len(datasets) == 8
    assert [dataset.dimension for dataset in datasets] == [2, 2, 3, 4, 4, 5, 6, 8]


def test_surrogate_predicts_finite_mean_and_uncertainty() -> None:
    dataset = load_datasets()[0]
    model = GaussianProcessSurrogate().fit(dataset.x, dataset.y)
    mean, std = model.predict(dataset.x[:2])
    assert np.all(np.isfinite(mean))
    assert np.all(std >= 0)


def test_acquisitions_have_expected_shape() -> None:
    mean = np.array([0.2, 0.4])
    std = np.array([0.1, 0.3])
    assert ucb(mean, std).shape == (2,)
    assert expected_improvement(mean, std, incumbent=0.5).shape == (2,)
    assert np.allclose(posterior_variance(std), np.array([0.01, 0.09]))


def test_proposal_is_in_domain_and_unseen() -> None:
    dataset = load_datasets()[3]
    proposal, _, _ = propose_query(dataset, seed=12)
    assert proposal.shape == (dataset.dimension,)
    assert np.all((proposal >= 0.000001) & (proposal <= 0.999999))
    assert not any(np.allclose(proposal, observed) for observed in dataset.x)


def test_experiment_result_contains_stability_metric() -> None:
    result = run_experiment(load_datasets()[7])
    assert result.loo_rank_mae >= 0.0
