import math

import pytest

from quantmath.pricing import black_scholes_call, black_scholes_put


def test_black_scholes_call_reference_value():
    price = black_scholes_call(100.0, 100.0, 0.05, 0.20, 1.0)
    assert price == pytest.approx(10.45058357, abs=1e-8)


def test_put_call_parity():
    spot, strike, rate, volatility, maturity = 100.0, 105.0, 0.03, 0.25, 2.0
    call = black_scholes_call(spot, strike, rate, volatility, maturity)
    put = black_scholes_put(spot, strike, rate, volatility, maturity)
    expected = spot - strike * math.exp(-rate * maturity)
    assert call - put == pytest.approx(expected, abs=1e-10)


@pytest.mark.parametrize(
    ("spot", "strike", "volatility", "maturity"),
    [(0.0, 100.0, 0.20, 1.0), (100.0, -1.0, 0.20, 1.0), (100.0, 100.0, 0.0, 1.0)],
)
def test_black_scholes_rejects_non_positive_domain(spot, strike, volatility, maturity):
    with pytest.raises(ValueError):
        black_scholes_call(spot, strike, 0.05, volatility, maturity)


def test_black_scholes_rejects_non_finite_inputs():
    with pytest.raises(ValueError, match="finite"):
        black_scholes_call(100.0, 100.0, float("nan"), 0.20, 1.0)
