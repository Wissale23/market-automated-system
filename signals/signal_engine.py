import pandas as pd


def generate_signals(
    df: pd.DataFrame,
    ma_short: int = 5,
    ma_long: int = 20
):

    df = df.copy()

    short_col = f"ma_{ma_short}"
    long_col = f"ma_{ma_long}"


    if short_col not in df.columns:
        raise ValueError(
            f"Missing column: {short_col}"
        )

    if long_col not in df.columns:
        raise ValueError(
            f"Missing column: {long_col}"
        )


    df["signal"] = 0


    # BUY
    df.loc[
        df[short_col] > df[long_col],
        "signal"
    ] = 1


    # SELL
    df.loc[
        df[short_col] < df[long_col],
        "signal"
    ] = -1


    return df