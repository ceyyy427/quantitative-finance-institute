import numpy as np
import pytest

from quantmath.time_series import autocorrelation, fit_ar1, log_returns


def test_log_returns_and_ar1_fit():
    prices = np.array([100.0, 110.0, 121.0])
    assert log_returns(prices) == pytest.approx(np.log([1.1, 1.1]))

    values = np.array([1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125])
    fitted = fit_ar1(values)
    assert fitted.coefficient == pytest.approx(0.5, abs=0.1)
    assert autocorrelation(values, lag=1) > 0
