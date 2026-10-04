import numpy as np
import pytest

from quantmath.hedging import DeltaHedgeResult, simulate_delta_hedge


def _run(seed: int = 7) -> DeltaHedgeResult:
    return simulate_delta_hedge(
        spot=100.0,
        strike=100.0,
        rate=0.05,
        volatility=0.20,
        maturity=1.0,
        steps=12,
        seed=seed,
    )


@pytest.mark.parametrize(
    ("name", "value"),
    [
        ("spot", 0.0),
        ("strike", -1.0),
        ("volatility", 0.0),
        ("maturity", -0.1),
        ("steps", 0),
    ],
)
def test_delta_hedge_rejects_invalid_inputs(name: str, value: float) -> None:
    kwargs = {
        "spot": 100.0,
        "strike": 100.0,
        "rate": 0.05,
        "volatility": 0.20,
        "maturity": 1.0,
        "steps": 12,
    }
    kwargs[name] = value

    with pytest.raises(ValueError):
        simulate_delta_hedge(**kwargs)


def test_delta_hedge_is_reproducible_for_a_seed() -> None:
    first = _run(seed=11)
    second = _run(seed=11)

    assert first == second
    assert np.array_equal(first.path, second.path)
    assert first.path.shape == (13,)
    assert first.rebalancing_steps == 12


def test_delta_hedge_result_contains_option_payoff_and_pnl() -> None:
    result = _run()

    assert isinstance(result, DeltaHedgeResult)
    assert result.terminal_spot == pytest.approx(result.path[-1])
    assert result.option_payoff >= 0.0
    assert result.initial_option_value > 0.0
    assert np.isfinite(result.hedge_pnl)


def test_put_delta_hedge_has_put_payoff() -> None:
    result = simulate_delta_hedge(
        spot=100.0,
        strike=100.0,
        rate=0.05,
        volatility=0.20,
        maturity=1.0,
        steps=4,
        seed=3,
        option="put",
    )

    assert result.option_payoff == pytest.approx(max(100.0 - result.terminal_spot, 0.0))


def test_delta_hedge_rejects_unknown_option() -> None:
    with pytest.raises(ValueError, match="option"):
        simulate_delta_hedge(
            spot=100.0,
            strike=100.0,
            rate=0.05,
            volatility=0.20,
            maturity=1.0,
            steps=4,
            option="straddle",
        )
