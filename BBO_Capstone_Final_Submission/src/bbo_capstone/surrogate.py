"""Small, dependency-light Gaussian-process surrogate and acquisitions.

The implementation deliberately favours transparency over a large model zoo. The
observed outputs are rank-normalised before fitting so functions with very
different output scales can use the same stable optimisation machinery.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import erf, pi, sqrt

import numpy as np


def rank_normalize(values: np.ndarray) -> np.ndarray:
    """Map objective values to [0, 1] while preserving their ordering."""
    order = np.argsort(np.argsort(values, kind="stable"), kind="stable")
    if len(values) == 1:
        return np.zeros(1, dtype=float)
    return order.astype(float) / (len(values) - 1)


@dataclass
class GaussianProcessSurrogate:
    """Gaussian process with a fixed isotropic RBF kernel.

    Fixing the length scale is intentional: only 11 observations per function
    are available, so unconstrained kernel optimisation would be unstable.
    """

    length_scale: float = 0.22
    noise: float = 5e-2

    def fit(self, x: np.ndarray, y: np.ndarray) -> "GaussianProcessSurrogate":
        self.x_train = np.asarray(x, dtype=float)
        self.y_train = rank_normalize(np.asarray(y, dtype=float))
        self.prior_mean = float(np.mean(self.y_train))
        squared_distance = _squared_distance(self.x_train, self.x_train)
        kernel = np.exp(-0.5 * squared_distance / self.length_scale**2)
        kernel += np.eye(len(self.x_train)) * self.noise
        self.cholesky = np.linalg.cholesky(kernel)
        centred_targets = self.y_train - self.prior_mean
        self.alpha = np.linalg.solve(self.cholesky.T, np.linalg.solve(self.cholesky, centred_targets))
        return self

    def predict(self, x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        candidates = np.asarray(x, dtype=float)
        squared_distance = _squared_distance(candidates, self.x_train)
        cross_kernel = np.exp(-0.5 * squared_distance / self.length_scale**2)
        # Rank targets are bounded. Clipping prevents far-away extrapolation from
        # being mistaken for an implausibly certain score above the best rank.
        mean = np.clip(self.prior_mean + cross_kernel @ self.alpha, 0.0, 1.0)
        projected = np.linalg.solve(self.cholesky, cross_kernel.T)
        variance = np.maximum(1.0 - np.sum(projected**2, axis=0), 1e-12)
        return mean, np.sqrt(variance)


def ucb(mean: np.ndarray, std: np.ndarray, kappa: float = 0.25) -> np.ndarray:
    """Upper confidence bound: higher kappa favours unexplored regions."""
    return mean + kappa * std


def expected_improvement(mean: np.ndarray, std: np.ndarray, incumbent: float) -> np.ndarray:
    """Expected improvement under a Gaussian predictive approximation."""
    improvement = mean - incumbent
    safe_std = np.maximum(std, 1e-12)
    z = improvement / safe_std
    normal_pdf = np.exp(-0.5 * z**2) / sqrt(2.0 * pi)
    normal_cdf = 0.5 * (1.0 + np.vectorize(erf)(z / sqrt(2.0)))
    return improvement * normal_cdf + safe_std * normal_pdf


def posterior_variance(std: np.ndarray) -> np.ndarray:
    """Pure-exploration acquisition based on posterior variance."""
    return std**2


def _squared_distance(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    difference = left[:, None, :] - right[None, :, :]
    return np.sum(difference**2, axis=2)
