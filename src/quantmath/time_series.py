"""Basic return and AR(1) helpers for the time-series chapter."""

from dataclasses import dataclass

import numpy as np


def log_returns(prices: np.ndarray) -> np.ndarray:
    prices = np.asarray(prices, dtype=float)
    if prices.size < 2 or np.any(prices <= 0):
        raise ValueError("prices must contain at least two positive values")
    return np.diff(np.log(prices))


def autocorrelation(values: np.ndarray, lag: int = 1) -> float:
    values = np.asarray(values, dtype=float)
    if lag <= 0 or lag >= values.size:
        raise ValueError("lag must be positive and smaller than the sample size")
    centered = values - values.mean()
    denominator = centered @ centered
    if np.isclose(denominator, 0.0):
        raise ValueError("autocorrelation is undefined for a constant series")
    return float(centered[:-lag] @ centered[lag:] / denominator)


@dataclass(frozen=True)
class AR1Fit:
    intercept: float
    coefficient: float
    residual_std: float


def fit_ar1(values: np.ndarray) -> AR1Fit:
    values = np.asarray(values, dtype=float)
    if values.size < 3:
        raise ValueError("at least three observations are required")
    design = np.column_stack([np.ones(values.size - 1), values[:-1]])
    coefficients, *_ = np.linalg.lstsq(design, values[1:], rcond=None)
    residuals = values[1:] - design @ coefficients
    residual_std = float(np.sqrt(np.sum(residuals**2) / max(values.size - 3, 1)))
    return AR1Fit(float(coefficients[0]), float(coefficients[1]), residual_std)
