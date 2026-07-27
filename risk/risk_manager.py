import pandas as pd
from config.config import MAX_POSITION, STOP_LOSS

def apply_risk_management(df):
    """
    Controls position size and applies stop loss.
    """

    df = df.copy()

    # Find ticker-specific close column
    close_col = [col for col in df.columns if col.startswith("close_")][0]

    df["position"] = 0

    for i in range(1, len(df)):

        previous_position = df.loc[df.index[i-1], "position"]
        signal = df.loc[df.index[i], "signal"]

        if signal == 1:
            df.loc[df.index[i], "position"] = MAX_POSITION

        elif signal == -1:
            df.loc[df.index[i], "position"] = 0

        else:
            df.loc[df.index[i], "position"] = previous_position


    entry_price = None

    for i in range(len(df)):

        if df.loc[df.index[i], "position"] > 0:

            if entry_price is None:
                entry_price = df.loc[df.index[i], close_col]

            current_price = df.loc[df.index[i], close_col]

            loss = (current_price - entry_price) / entry_price

            if loss < -STOP_LOSS:
                df.loc[df.index[i], "position"] = 0
                entry_price = None

        else:
            entry_price = None


    return df