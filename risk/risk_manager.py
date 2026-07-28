import pandas as pd


def apply_risk_management(
    df,
    max_position=1.0,
    stop_loss=0.05
):
    """
    Applies position sizing and stop loss.

    Parameters:
        max_position:
            Maximum allocation (1.0 = 100%)

        stop_loss:
            Maximum loss allowed before exiting position
            Example: 0.05 = 5%
    """

    df = df.copy()

    df["position"] = 0


    # -------------------------
    # Position management
    # -------------------------

    for i in range(1, len(df)):

        previous_position = df.loc[
            df.index[i-1],
            "position"
        ]

        signal = df.loc[
            df.index[i],
            "signal"
        ]


        if signal == 1:
            df.loc[
                df.index[i],
                "position"
            ] = max_position


        elif signal == -1:
            df.loc[
                df.index[i],
                "position"
            ] = 0


        else:
            df.loc[
                df.index[i],
                "position"
            ] = previous_position



    # -------------------------
    # Stop loss
    # -------------------------

    price_col = [
        c for c in df.columns
        if c.startswith("close_")
    ][0]


    entry_price = None


    for i in range(len(df)):

        position = df.loc[
            df.index[i],
            "position"
        ]

        current_price = df.loc[
            df.index[i],
            price_col
        ]


        # entering trade
        if position > 0:

            if entry_price is None:
                entry_price = current_price


            loss = (
                current_price - entry_price
            ) / entry_price


            # stop loss triggered
            if loss < -stop_loss:

                df.loc[
                    df.index[i],
                    "position"
                ] = 0

                entry_price = None


        else:
            entry_price = None


    return df