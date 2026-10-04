from quantmath import DeltaHedgeResult, __version__, simulate_delta_hedge


def test_package_version():
    assert __version__ == "0.4.0"


def test_public_hedging_api():
    result = simulate_delta_hedge(100.0, 100.0, 0.05, 0.20, 1.0, 2, seed=1)
    assert isinstance(result, DeltaHedgeResult)
