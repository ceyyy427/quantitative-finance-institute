import numpy as np
import pytest

from quantmath.portfolio import minimum_variance_weights, portfolio_return
from quantmath.risk import historical_cvar, historical_var, normal_cvar, normal_var


def test_markowitz_constraints_are_satisfied():
    means = np.array([0.08, 0.12])
    covariance = np.array([[0.04, 0.01], [0.01, 0.09]])
    weights = minimum_variance_weights(means, covariance, target_return=0.10)
    assert weights.sum() == pytest.approx(1.0)
    assert portfolio_return(weights, means) == pytest.approx(0.10)


def test_historical_var_and_cvar_use_positive_losses():
    returns = np.array([-0.10, -0.05, 0.00, 0.02, 0.03])
    assert historical_var(returns, level=0.80) == pytest.approx(0.06)
    assert historical_cvar(returns, level=0.80) == pytest.approx(0.10)


def test_normal_cvar_exceeds_normal_var():
    var = normal_var(0.0, 0.02, level=0.95)
    cvar = normal_cvar(0.0, 0.02, level=0.95)
    assert cvar > var
