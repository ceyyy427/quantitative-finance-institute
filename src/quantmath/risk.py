"""Historical and normal-model VaR/CVaR calculations."""

import math
from statistics import NormalDist

import numpy as np


def historical_var(returns: np.ndarray, level: float = 0.95) -> float:
    """Return positive loss VaR from a vector of simple returns."""

    losses = -np.asarray(returns, dtype=float)
    if losses.size == 0 or not 0 < level < 1:
        raise ValueError("returns must be non-empty and level must lie in (0, 1)")
    return float(np.quantile(losses, level))


def historical_cvar(returns: np.ndarray, level: float = 0.95) -> float:
    """Return the mean loss conditional on exceeding historical VaR."""

    losses = -np.asarray(returns, dtype=float)
    var = historical_var(returns, level)
    tail = losses[losses >= var]
    return float(tail.mean())


def normal_var(mean_return: float, volatility: float, level: float = 0.95) -> float:
    """Return positive loss VaR under a normal return model."""

    if volatility < 0 or not 0 < level < 1:
        raise ValueError("volatility must be non-negative and level must lie in (0, 1)")
    z = NormalDist().inv_cdf(level)
    return -mean_return + volatility * z


def normal_cvar(mean_return: float, volatility: float, level: float = 0.95) -> float:
    """Return normal-model expected shortfall for positive losses."""

    if volatility < 0 or not 0 < level < 1:
        raise ValueError("volatility must be non-negative and level must lie in (0, 1)")
    z = NormalDist().inv_cdf(level)
    density = math.exp(-0.5 * z**2) / math.sqrt(2 * math.pi)
    return -mean_return + volatility * density / (1 - level)
