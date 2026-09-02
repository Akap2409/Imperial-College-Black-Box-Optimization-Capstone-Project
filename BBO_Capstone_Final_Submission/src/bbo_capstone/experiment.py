"""Candidate design, model checks, and sequential query proposals."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np

from .data import FunctionDataset
from .surrogate import GaussianProcessSurrogate, expected_improvement, posterior_variance, rank_normalize, ucb

AcquisitionName = Literal["ucb", "ei", "variance"]
LOWER_BOUND = 0.000001
UPPER_BOUND = 0.999999


@dataclass(frozen=True)
class ExperimentResult:
    function: str
    dimension: int
    acquisition: AcquisitionName
    proposal: np.ndarray
    predicted_rank: float
    predicted_uncertainty: float
    best_observed_value: float
    best_observed_point: np.ndarray
    loo_rank_mae: float


def generate_candidates(dataset: FunctionDataset, *, seed: int, global_count: int = 6000) -> np.ndarray:
    """Mix global coverage with local refinement around the three best points."""
    rng = np.random.default_rng(seed)
    global_candidates = rng.uniform(LOWER_BOUND, UPPER_BOUND, size=(global_count, dataset.dimension))
    elite_indices = np.argsort(dataset.y)[-min(3, len(dataset.y)) :]
    local_parts = []
    for index in elite_indices:
        local_parts.append(
            np.clip(
                dataset.x[index] + rng.normal(0.0, 0.075, size=(1200, dataset.dimension)),
                LOWER_BOUND,
                UPPER_BOUND,
            )
        )
    candidates = np.vstack([global_candidates, *local_parts, dataset.x])
    return _remove_seen_candidates(candidates, dataset.x)


def propose_query(
    dataset: FunctionDataset,
    acquisition: AcquisitionName = "ucb",
    *,
    seed: int = 42,
) -> tuple[np.ndarray, float, float]:
    """Fit a surrogate and return a candidate selected by the chosen acquisition."""
    model = GaussianProcessSurrogate().fit(dataset.x, dataset.y)
    candidates = generate_candidates(dataset, seed=seed)
    mean, std = model.predict(candidates)

    if acquisition == "ucb":
        score = ucb(mean, std)
    elif acquisition == "ei":
        score = expected_improvement(mean, std, incumbent=1.0)
    elif acquisition == "variance":
        score = posterior_variance(std)
    else:
        raise ValueError(f"Unsupported acquisition: {acquisition}")

    selected = int(np.argmax(score))
    return candidates[selected], float(mean[selected]), float(std[selected])


def leave_one_out_rank_mae(dataset: FunctionDataset) -> float:
    """Estimate surrogate stability with leave-one-out rank prediction error."""
    observed_ranks = rank_normalize(dataset.y)
    errors: list[float] = []
    for held_out in range(len(dataset.y)):
        keep = np.arange(len(dataset.y)) != held_out
        model = GaussianProcessSurrogate().fit(dataset.x[keep], dataset.y[keep])
        predicted, _ = model.predict(dataset.x[held_out : held_out + 1])
        errors.append(abs(float(predicted[0]) - float(observed_ranks[held_out])))
    return float(np.mean(errors))


def run_experiment(dataset: FunctionDataset, acquisition: AcquisitionName = "ucb") -> ExperimentResult:
    """Run the reproducible retrospective proposal workflow for one function."""
    function_number = int(dataset.name.split(" ")[1])
    proposal, mean, std = propose_query(dataset, acquisition, seed=100 + function_number)
    return ExperimentResult(
        function=dataset.name,
        dimension=dataset.dimension,
        acquisition=acquisition,
        proposal=proposal,
        predicted_rank=mean,
        predicted_uncertainty=std,
        best_observed_value=dataset.best_value,
        best_observed_point=dataset.best_point,
        loo_rank_mae=leave_one_out_rank_mae(dataset),
    )


def _remove_seen_candidates(candidates: np.ndarray, observed: np.ndarray) -> np.ndarray:
    distances = np.sqrt(np.min(np.sum((candidates[:, None, :] - observed[None, :, :]) ** 2, axis=2), axis=1))
    return candidates[distances > 1e-8]
