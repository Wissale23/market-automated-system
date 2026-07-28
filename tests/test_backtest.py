from ingestion.fetch_data import fetch_stock_data
from features.feature_engineering import add_basic_features
from signals.signal_engine import generate_signals
from risk.risk_manager import apply_risk_management
from backtest.backtest_engine import run_backtest


def test_backtest_columns():

    df = fetch_stock_data("AAPL")
    df = add_basic_features(df)
    df = generate_signals(df)
    df = apply_risk_management(df)

    df, metrics = run_backtest(df)

    expected = [
        "portfolio_value",
        "buy_hold_value",
        "strategy_return",
        "market_return"
    ]

    for col in expected:
        assert col in df.columns


def test_metrics_exist():

    df = fetch_stock_data("AAPL")
    df = add_basic_features(df)
    df = generate_signals(df)
    df = apply_risk_management(df)

    df, metrics = run_backtest(df)

    expected = [
        "sharpe_ratio",
        "max_drawdown",
        "win_rate",
        "buy_hold_return_total",
        "strategy_return_total"
    ]

    for key in expected:
        assert key in metrics


def test_portfolio_positive():

    df = fetch_stock_data("AAPL")
    df = add_basic_features(df)
    df = generate_signals(df)
    df = apply_risk_management(df)

    df, metrics = run_backtest(df)

    assert (df["portfolio_value"] > 0).all()