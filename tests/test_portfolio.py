from ingestion.fetch_data import fetch_stock_data
from features.feature_engineering import add_basic_features
from signals.signal_engine import generate_signals
from risk.risk_manager import apply_risk_management
from backtest.backtest_engine import run_backtest

from portfolio.optimizer import (
    equal_weight,
    volatility_weight,
    minimum_variance,
    maximum_sharpe
)


def create_results():

    tickers = [
        "AAPL",
        "MSFT",
        "GOOG"
    ]

    results = {}

    for ticker in tickers:

        df = fetch_stock_data(ticker)
        df = add_basic_features(df)
        df = generate_signals(df)
        df = apply_risk_management(df)
        df, metrics = run_backtest(df)

        results[ticker] = {
            "data": df,
            "metrics": metrics
        }

    return results


def test_equal_weights():

    results = create_results()

    weights = equal_weight(results)

    assert abs(sum(weights.values()) - 1) < 1e-6


def test_volatility_weights():

    results = create_results()

    weights = volatility_weight(results)

    assert abs(sum(weights.values()) - 1) < 1e-6


def test_minimum_variance():

    results = create_results()

    weights = minimum_variance(results)

    assert abs(sum(weights.values()) - 1) < 1e-6


def test_maximum_sharpe():

    results = create_results()

    weights = maximum_sharpe(results)

    assert abs(sum(weights.values()) - 1) < 1e-6