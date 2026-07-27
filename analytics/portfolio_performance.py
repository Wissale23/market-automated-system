import numpy as np


def calculate_portfolio_metrics(equity_curve):

    returns = equity_curve.pct_change().dropna()

    sharpe = (
        returns.mean()
        /
        returns.std()
        *
        np.sqrt(252)
    )

    volatility = returns.std() * np.sqrt(252)

    drawdown = (
        equity_curve /
        equity_curve.cummax()
        - 1
    )

    return {
        "total_return": (
            equity_curve.iloc[-1]
            /
            equity_curve.iloc[0]
            - 1
        ),

        "volatility": volatility,

        "sharpe_ratio": sharpe,

        "max_drawdown": drawdown.min()
    }