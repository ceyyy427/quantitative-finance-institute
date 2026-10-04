"""Closed-form pricing formulas used in the teaching chapters."""

import math
from statistics import NormalDist

_STANDARD_NORMAL = NormalDist()


def _validate_inputs(spot: float, strike: float, rate: float, volatility: float, maturity: float) -> None:
    if spot <= 0 or strike <= 0:
        raise ValueError("spot and strike must be positive")
    if volatility <= 0:
        raise ValueError("volatility must be positive")
    if maturity <= 0:
        raise ValueError("maturity must be positive")
    if not all(math.isfinite(value) for value in (spot, strike, rate, volatility, maturity)):
        raise ValueError("all inputs must be finite")


def black_scholes_call(
    spot: float,
    strike: float,
    rate: float,
    volatility: float,
    maturity: float,
) -> float:
    """Price a European call under the Black–Scholes assumptions.

    Parameters use continuously compounded risk-free rate and annualized
    volatility. The formula assumes no dividends and a positive maturity.
    """

    _validate_inputs(spot, strike, rate, volatility, maturity)
    root_t = math.sqrt(maturity)
    d1 = (math.log(spot / strike) + (rate + 0.5 * volatility**2) * maturity) / (
        volatility * root_t
    )
    d2 = d1 - volatility * root_t
    return spot * _STANDARD_NORMAL.cdf(d1) - strike * math.exp(-rate * maturity) * _STANDARD_NORMAL.cdf(d2)


def black_scholes_put(
    spot: float,
    strike: float,
    rate: float,
    volatility: float,
    maturity: float,
) -> float:
    """Price a European put using put–call parity."""

    call = black_scholes_call(spot, strike, rate, volatility, maturity)
    return call - spot + strike * math.exp(-rate * maturity)
