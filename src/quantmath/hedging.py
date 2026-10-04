"""Discrete-time delta-hedging simulation for teaching and experiments."""

import math
from dataclasses import dataclass
from typing import Literal

import numpy as np

from .greeks import call_delta, put_delta
from .pricing import black_scholes_call, black_scholes_put


@dataclass(frozen=True)
class DeltaHedgeResult:
    """Summary of a short-option replication hedge along one simulated path."""

    terminal_spot: float
    option_payoff: float
    initial_option_value: float
    hedge_pnl: float
    rebalancing_steps: int
    path: np.ndarray

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DeltaHedgeResult):
            return NotImplemented
        return (
            self.terminal_spot == other.terminal_spot
            and self.option_payoff == other.option_payoff
            and self.initial_option_value == other.initial_option_value
            and self.hedge_pnl == other.hedge_pnl
            and self.rebalancing_steps == other.rebalancing_steps
            and np.array_equal(self.path, other.path)
        )


def _validate_inputs(
    spot: float,
    strike: float,
    rate: float,
    volatility: float,
    maturity: float,
    steps: int,
    option: str,
) -> None:
    if spot <= 0 or strike <= 0:
        raise ValueError("spot and strike must be positive")
    if volatility <= 0:
        raise ValueError("volatility must be positive")
    if maturity <= 0:
        raise ValueError("maturity must be positive")
    if not isinstance(steps, int) or isinstance(steps, bool) or steps <= 0:
        raise ValueError("steps must be a positive integer")
    if option not in {"call", "put"}:
        raise ValueError("option must be 'call' or 'put'")
    if not all(math.isfinite(value) for value in (spot, strike, rate, volatility, maturity)):
        raise ValueError("all numeric inputs must be finite")


def _price_and_delta(
    spot: float,
    strike: float,
    rate: float,
    volatility: float,
    maturity: float,
    option: Literal["call", "put"],
) -> tuple[float, float]:
    if option == "call":
        return (
            black_scholes_call(spot, strike, rate, volatility, maturity),
            call_delta(spot, strike, rate, volatility, maturity),
        )
    return (
        black_scholes_put(spot, strike, rate, volatility, maturity),
        put_delta(spot, strike, rate, volatility, maturity),
    )


def simulate_delta_hedge(
    spot: float,
    strike: float,
    rate: float,
    volatility: float,
    maturity: float,
    steps: int,
    seed: int | None = None,
    option: Literal["call", "put"] = "call",
) -> DeltaHedgeResult:
    """Simulate a self-financing hedge for one short European option.

    The hedge sells the option for its Black–Scholes value, buys the option
    delta in the underlying, and keeps the remainder in a continuously
    compounded cash account. The returned ``hedge_pnl`` is terminal hedge
    value minus the option payoff; positive values are hedge surplus.
    """

    _validate_inputs(spot, strike, rate, volatility, maturity, steps, option)
    dt = maturity / steps
    growth = math.exp(rate * dt)
    root_dt = math.sqrt(dt)
    rng = np.random.default_rng(seed)
    path = np.empty(steps + 1, dtype=float)
    path[0] = spot
    shocks = rng.standard_normal(steps)
    drift = (rate - 0.5 * volatility**2) * dt
    diffusion = volatility * root_dt
    for index, shock in enumerate(shocks, start=1):
        path[index] = path[index - 1] * math.exp(drift + diffusion * float(shock))

    initial_value, shares = _price_and_delta(spot, strike, rate, volatility, maturity, option)
    cash = initial_value - shares * spot

    for index in range(1, steps + 1):
        cash *= growth
        if index == steps:
            continue
        remaining = maturity - index * dt
        _, new_shares = _price_and_delta(
            float(path[index]), strike, rate, volatility, remaining, option
        )
        cash -= (new_shares - shares) * path[index]
        shares = new_shares

    terminal_spot = float(path[-1])
    if option == "call":
        payoff = max(terminal_spot - strike, 0.0)
    else:
        payoff = max(strike - terminal_spot, 0.0)
    terminal_hedge_value = cash + shares * terminal_spot
    return DeltaHedgeResult(
        terminal_spot=terminal_spot,
        option_payoff=payoff,
        initial_option_value=initial_value,
        hedge_pnl=terminal_hedge_value - payoff,
        rebalancing_steps=steps,
        path=path,
    )
