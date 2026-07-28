import pandas as pd

from ingestion.fetch_data import fetch_stock_data
from features.feature_engineering import add_basic_features


def test_feature_columns_exist():

    df = fetch_stock_data("AAPL")
    df = add_basic_features(df)

    expected = [
        "returns",
        "ma_5",
        "ma_20",
        "volatility_20",
        "momentum",
        "rsi",
        "ema_20",
        "ema_50",
        "macd",
        "macd_signal"
    ]

    for column in expected:
        assert column in df.columns


def test_no_missing_values():

    df = fetch_stock_data("AAPL")
    df = add_basic_features(df)

    assert df.isnull().sum().sum() == 0


def test_returns_are_numeric():

    df = fetch_stock_data("AAPL")
    df = add_basic_features(df)

    assert pd.api.types.is_numeric_dtype(df["returns"])