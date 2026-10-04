"""Small, transparent mean–variance portfolio calculations."""

import numpy as np


def portfolio_return(weights: np.ndarray, expected_returns: np.ndarray) -> float:
    return float(np.asarray(weights) @ np.asarray(expected_returns))


def portfolio_volatility(weights: np.ndarray, covariance: np.ndarray) -> float:
    weights = np.asarray(weights)
    covariance = np.asarray(covariance)
    return float(np.sqrt(weights @ covariance @ weights))


def minimum_variance_weights(
    expected_returns: np.ndarray,
    covariance: np.ndarray,
    target_return: float,
) -> np.ndarray:
    """Return unconstrained Markowitz weights for a target return.

    The solution allows short selling. Long-only constraints require a
    quadratic-programming solver and are intentionally kept separate.
    """

    expected_returns = np.asarray(expected_returns, dtype=float)
    covariance = np.asarray(covariance, dtype=float)
    n_assets = expected_returns.size
    if covariance.shape != (n_assets, n_assets):
        raise ValueError("covariance must be a square matrix matching expected_returns")
    if not np.allclose(covariance, covariance.T):
        raise ValueError("covariance must be symmetric")

    inv_covariance = np.linalg.inv(covariance)
    ones = np.ones(n_assets)
    a = ones @ inv_covariance @ ones
    b = ones @ inv_covariance @ expected_returns
    c = expected_returns @ inv_covariance @ expected_returns
    determinant = a * c - b**2
    if np.isclose(determinant, 0.0):
        raise ValueError("target and budget constraints are not independent")

    multiplier_budget = (c - b * target_return) / determinant
    multiplier_return = (a * target_return - b) / determinant
    return inv_covariance @ (multiplier_budget * ones + multiplier_return * expected_returns)
