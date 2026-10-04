"""Monte Carlo estimators for simple risk-neutral pricing examples."""

import math

import numpy as np


def european_call_monte_carlo(
    spot: float,
    strike: float,
    rate: float,
    volatility: float,
    maturity: float,
    paths: int = 100_000,
    seed: int = 42,
) -> tuple[float, float]:
    """Estimate a European call price and its standard error.

    The terminal stock price is sampled under the risk-neutral GBM model.
    The returned standard error is the Monte Carlo standard error of the
    discounted payoff estimate.
    """

    if spot <= 0 or strike <= 0:
        raise ValueError("spot and strike must be positive")
    if volatility <= 0 or maturity <= 0:
        raise ValueError("volatility and maturity must be positive")
    if not isinstance(paths, (int, np.integer)) or isinstance(paths, bool) or paths < 2:
        raise ValueError("paths must be an integer of at least 2")
    if not all(math.isfinite(value) for value in (spot, strike, rate, volatility, maturity)):
        raise ValueError("all inputs must be finite")

    rng = np.random.default_rng(seed)
    shocks = rng.standard_normal(paths)
    terminal = spot * np.exp(
        (rate - 0.5 * volatility**2) * maturity
        + volatility * math.sqrt(maturity) * shocks
    )
    discounted_payoffs = math.exp(-rate * maturity) * np.maximum(terminal - strike, 0.0)
    price = float(discounted_payoffs.mean())
    standard_error = float(discounted_payoffs.std(ddof=1) / math.sqrt(paths))
    return price, standard_error
