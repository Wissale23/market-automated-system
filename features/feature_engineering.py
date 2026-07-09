import pandas as pd

from features.technical_indicators import (
    get_close_column,
    add_moving_averages,
    add_volatility,
    add_momentum,
    add_rsi,
    add_ema,
    add_macd
)


def add_basic_features(df: pd.DataFrame):

    df = df.copy()

    close_col = get_close_column(df)

    # Basic return feature
    df["returns"] = df[close_col].pct_change()


    # Technical indicators
    df = add_moving_averages(df)

    df = add_volatility(df)

    df = add_momentum(df)

    df = add_rsi(df)

    df = add_ema(df)

    df = add_macd(df)


    # Remove NaN created by rolling calculations
    df.dropna(inplace=True)


    return df