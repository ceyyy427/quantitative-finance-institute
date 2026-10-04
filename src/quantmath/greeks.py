"""Analytic Black–Scholes sensitivities for European options."""

import math
from statistics import NormalDist

_NORMAL = NormalDist()


def _d1_d2(spot: float, strike: float, rate: float, volatility: float, maturity: float) -> tuple[float, float]:
    if spot <= 0 or strike <= 0 or volatility <= 0 or maturity <= 0:
        raise ValueError("spot, strike, volatility, and maturity must be positive")
    if not all(math.isfinite(value) for value in (spot, strike, rate, volatility, maturity)):
        raise ValueError("all inputs must be finite")
    root_t = math.sqrt(maturity)
    d1 = (math.log(spot / strike) + (rate + 0.5 * volatility**2) * maturity) / (volatility * root_t)
    return d1, d1 - volatility * root_t


def _phi(value: float) -> float:
    return math.exp(-0.5 * value**2) / math.sqrt(2 * math.pi)


def call_delta(spot: float, strike: float, rate: float, volatility: float, maturity: float) -> float:
    d1, _ = _d1_d2(spot, strike, rate, volatility, maturity)
    return _NORMAL.cdf(d1)


def put_delta(spot: float, strike: float, rate: float, volatility: float, maturity: float) -> float:
    return call_delta(spot, strike, rate, volatility, maturity) - 1.0


def gamma(spot: float, strike: float, rate: float, volatility: float, maturity: float) -> float:
    d1, _ = _d1_d2(spot, strike, rate, volatility, maturity)
    return _phi(d1) / (spot * volatility * math.sqrt(maturity))


def vega(spot: float, strike: float, rate: float, volatility: float, maturity: float) -> float:
    d1, _ = _d1_d2(spot, strike, rate, volatility, maturity)
    return spot * _phi(d1) * math.sqrt(maturity)


def call_theta(spot: float, strike: float, rate: float, volatility: float, maturity: float) -> float:
    d1, d2 = _d1_d2(spot, strike, rate, volatility, maturity)
    return (
        -spot * _phi(d1) * volatility / (2 * math.sqrt(maturity))
        - rate * strike * math.exp(-rate * maturity) * _NORMAL.cdf(d2)
    )


def put_theta(spot: float, strike: float, rate: float, volatility: float, maturity: float) -> float:
    d1, d2 = _d1_d2(spot, strike, rate, volatility, maturity)
    return (
        -spot * _phi(d1) * volatility / (2 * math.sqrt(maturity))
        + rate * strike * math.exp(-rate * maturity) * _NORMAL.cdf(-d2)
    )


def call_rho(spot: float, strike: float, rate: float, volatility: float, maturity: float) -> float:
    _, d2 = _d1_d2(spot, strike, rate, volatility, maturity)
    return strike * maturity * math.exp(-rate * maturity) * _NORMAL.cdf(d2)


def put_rho(spot: float, strike: float, rate: float, volatility: float, maturity: float) -> float:
    _, d2 = _d1_d2(spot, strike, rate, volatility, maturity)
    return -strike * maturity * math.exp(-rate * maturity) * _NORMAL.cdf(-d2)
