import pytest

from quantmath.monte_carlo import european_call_monte_carlo
from quantmath.pricing import black_scholes_call


def test_monte_carlo_is_close_to_black_scholes():
    estimate, standard_error = european_call_monte_carlo(
        100.0, 100.0, 0.05, 0.20, 1.0, paths=200_000, seed=7
    )
    reference = black_scholes_call(100.0, 100.0, 0.05, 0.20, 1.0)
    assert abs(estimate - reference) < 4 * standard_error


def test_monte_carlo_seed_is_deterministic():
    first = european_call_monte_carlo(100.0, 100.0, 0.05, 0.20, 1.0, paths=500, seed=3)
    second = european_call_monte_carlo(100.0, 100.0, 0.05, 0.20, 1.0, paths=500, seed=3)
    assert first == second


def test_monte_carlo_rejects_non_integer_paths():
    with pytest.raises(ValueError, match="integer"):
        european_call_monte_carlo(100.0, 100.0, 0.05, 0.20, 1.0, paths=10.5)
