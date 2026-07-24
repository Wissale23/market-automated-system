import numpy as np


def calculate_performance(df):

    returns = df["portfolio_value"].pct_change()

    total_return = (
        df["portfolio_value"].iloc[-1] /
        df["portfolio_value"].iloc[0]
    ) - 1


    volatility = returns.std() * np.sqrt(252)


    sharpe = 0

    if volatility != 0:
        sharpe = (
            returns.mean() * 252
        ) / volatility


    drawdown = (
        df["portfolio_value"] /
        df["portfolio_value"].cummax()
    ) - 1


    max_drawdown = drawdown.min()


    return {
        "Total Return": round(total_return,4),
        "Volatility": round(volatility,4),
        "Sharpe Ratio": round(sharpe,4),
        "Max Drawdown": round(max_drawdown,4)
    }