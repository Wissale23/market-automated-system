from ingestion.fetch_data import fetch_stock_data
from features.feature_engineering import add_basic_features
from signals.signal_engine import generate_signals


def test_signal_column_exists():

    df = fetch_stock_data("AAPL")
    df = add_basic_features(df)
    df = generate_signals(df)

    assert "signal" in df.columns


def test_signal_values():

    df = fetch_stock_data("AAPL")
    df = add_basic_features(df)
    df = generate_signals(df)

    valid = {-1, 0, 1}

    assert set(df["signal"].unique()).issubset(valid)


def test_signals_not_empty():

    df = fetch_stock_data("AAPL")
    df = add_basic_features(df)
    df = generate_signals(df)

    assert len(df) > 0