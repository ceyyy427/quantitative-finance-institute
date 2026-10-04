import pytest

from quantmath.greeks import call_delta, gamma, vega


def test_at_the_money_greeks_reference_values():
    args = (100.0, 100.0, 0.05, 0.20, 1.0)
    assert call_delta(*args) == pytest.approx(0.63683065, abs=1e-7)
    assert gamma(*args) == pytest.approx(0.01876202, abs=1e-7)
    assert vega(*args) == pytest.approx(37.52403, abs=1e-4)
