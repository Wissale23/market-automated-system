import pandas as pd


def apply_risk_management(df, max_position=1.0, stop_loss=0.05):
    """
    Controls position size and applies stop loss.
    """

    df = df.copy()

    df["position"] = 0

    for i in range(1, len(df)):

        previous_position = df.loc[df.index[i-1], "position"]
        signal = df.loc[df.index[i], "signal"]

        if signal == 1:
            df.loc[df.index[i], "position"] = max_position

        elif signal == -1:
            df.loc[df.index[i], "position"] = 0

        else:
            df.loc[df.index[i], "position"] = previous_position


    entry_price = None

    for i in range(len(df)):

        if df.loc[df.index[i], "position"] > 0:

            if entry_price is None:
                entry_price = df.loc[df.index[i], "close_aapl"]

            current_price = df.loc[df.index[i], "close_aapl"]

            loss = (current_price - entry_price) / entry_price

            if loss < -stop_loss:
                df.loc[df.index[i], "position"] = 0
                entry_price = None

        else:
            entry_price = None


    return df