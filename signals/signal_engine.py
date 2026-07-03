import pandas as pd

def generate_signals(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # ensure correct columns exist
    required = ["ma_5", "ma_20"]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    # signal logic
    df["signal"] = 0

    df.loc[df["ma_5"] > df["ma_20"], "signal"] = 1   # BUY
    df.loc[df["ma_5"] < df["ma_20"], "signal"] = -1  # SELL

    return df