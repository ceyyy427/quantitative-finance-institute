from quantmath.monte_carlo import european_call_monte_carlo
from quantmath.pricing import black_scholes_call


def test_monte_carlo_is_close_to_black_scholes():
    estimate, standard_error = european_call_monte_carlo(
        100.0, 100.0, 0.05, 0.20, 1.0, paths=200_000, seed=7
    )
    reference = black_scholes_call(100.0, 100.0, 0.05, 0.20, 1.0)
    assert abs(estimate - reference) < 4 * standard_error
