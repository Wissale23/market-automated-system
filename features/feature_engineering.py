import pandas as pd

def add_basic_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # detect close column dynamically
    close_col = [c for c in df.columns if c.startswith("close")][0]

    df["returns"] = df[close_col].pct_change()
    df["ma_5"] = df[close_col].rolling(5).mean()
    df["ma_20"] = df[close_col].rolling(20).mean()
    df["volatility_20"] = df["returns"].rolling(20).std()
    df["momentum"] = df[close_col] / df[close_col].shift(5) - 1

    df.dropna(inplace=True)
    return df