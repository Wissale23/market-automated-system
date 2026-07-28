import pandas as pd

from features.technical_indicators import (
    add_moving_averages,
    add_volatility,
    add_momentum,
    add_rsi,
    add_ema,
    add_macd
)


def add_basic_features(
    df: pd.DataFrame,
    ma_short: int = 5,
    ma_long: int = 20
):
    
    df = df.copy()
    
    if ma_short >= ma_long:
        raise ValueError(
            "Short moving average must be smaller than long moving average"
        )

    
    close_col = [c for c in df.columns if c.startswith("close_")][0]


    # Basic return feature (modifieD)
    df["returns"] = df[close_col].pct_change(fill_method=None)


    # Technical indicators
    df = add_moving_averages(
        df,
        short_window=ma_short,
        long_window=ma_long
    )

    df = add_volatility(df)

    df = add_momentum(df)

    df = add_rsi(df)

    df = add_ema(df)

    df = add_macd(df)


    df.dropna(inplace=True)


    return df
