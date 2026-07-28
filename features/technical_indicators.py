import pandas as pd


def get_close_column(df):
    """
    Automatically finds the close price column.
    Works with AAPL, MSFT, etc.
    """
    close_cols = [c for c in df.columns if c.startswith("close")]

    if not close_cols:
        raise ValueError("No close price column found")

    return close_cols[0]


def add_moving_averages(
    df,
    short_window=5,
    long_window=20
):
    """
    Add simple moving averages.
    """

    df = df.copy()

    close_col = get_close_column(df)

    df[f"ma_{short_window}"] = (
        df[close_col]
        .rolling(short_window)
        .mean()
    )

    df[f"ma_{long_window}"] = (
        df[close_col]
        .rolling(long_window)
        .mean()
    )

    return df


def add_volatility(df):
    """
    Add rolling volatility.
    """

    df = df.copy()

    df["volatility_20"] = (
        df["returns"]
        .rolling(window=20)
        .std()
    )

    return df


def add_momentum(df):
    """
    Add price momentum.
    """

    df = df.copy()

    close_col = get_close_column(df)

    df["momentum"] = (
        df[close_col] /
        df[close_col].shift(5)
        - 1
    )

    return df


def add_rsi(df, period=14):
    """
    Relative Strength Index.
    """

    df = df.copy()

    close_col = get_close_column(df)

    delta = df[close_col].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    df["rsi"] = 100 - (100 / (1 + rs))

    return df


def add_ema(df):
    """
    Exponential moving averages.
    """

    df = df.copy()

    close_col = get_close_column(df)

    df["ema_20"] = (
        df[close_col]
        .ewm(span=20, adjust=False)
        .mean()
    )

    df["ema_50"] = (
        df[close_col]
        .ewm(span=50, adjust=False)
        .mean()
    )

    return df


def add_macd(df):
    """
    Moving Average Convergence Divergence.
    """

    df = df.copy()

    close_col = get_close_column(df)

    ema12 = (
        df[close_col]
        .ewm(span=12, adjust=False)
        .mean()
    )

    ema26 = (
        df[close_col]
        .ewm(span=26, adjust=False)
        .mean()
    )

    df["macd"] = ema12 - ema26

    df["macd_signal"] = (
        df["macd"]
        .ewm(span=9, adjust=False)
        .mean()
    )

    return df