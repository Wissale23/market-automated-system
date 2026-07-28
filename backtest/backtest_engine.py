import pandas as pd
import numpy as np


import numpy as np

def calculate_metrics(df):
    returns = df["strategy_return"].dropna()

    if returns.std() != 0:
        sharpe = np.sqrt(252) * returns.mean() / returns.std()
    else:
        sharpe = 0

    cumulative = (1 + returns).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak

    max_drawdown = drawdown.min()
    win_rate = (returns > 0).mean()
    volatility = returns.std() * np.sqrt(252)

    # -------------------------
    # BUY & HOLD METRICS
    # -------------------------
    buy_hold_return = df["buy_hold_return"].fillna(0)
    strategy_return = df["strategy_return"].fillna(0)

    buy_hold_total = (1 + buy_hold_return).prod() - 1
    strategy_total = (1 + strategy_return).prod() - 1

    return {
        "sharpe_ratio": sharpe,
        "volatility": volatility,
        "max_drawdown": max_drawdown,
        "win_rate": win_rate,
        "buy_hold_return_total": buy_hold_total,
        "strategy_return_total": strategy_total
    }
    
    

def run_backtest(
    df,
    initial_capital=10000,
    transaction_cost=0.001,
    slippage=0.0005
):

    df = df.copy()

    if "signal" not in df.columns:
        raise ValueError("Signal column missing")
    
    if "position" not in df.columns:
        raise ValueError("Position column missing")
    
    price_col = [c for c in df.columns if c.startswith("close")][0]

    # market returns
    df["market_return"] = df[price_col].pct_change(fill_method=None)

    # strategy returns 
    df["strategy_return"] = (
        df["position"].shift(1)
        *
        df["market_return"]
    )

    # -----------------------------
    # Transaction costs 
    # -----------------------------
    trades = df["signal"].diff().abs().fillna(0)
    total_cost = transaction_cost + slippage

    df["strategy_return"] -= total_cost * trades
    # equity curve
    df["equity_curve"] = (1 + df["strategy_return"].fillna(0)).cumprod()

    df["portfolio_value"] = initial_capital * df["equity_curve"]
    
    # -----------------------------
    # BUY & HOLD benchmark
    # -----------------------------
    df["buy_hold_return"] = df["market_return"].fillna(0)

    df["buy_hold_equity"] = (1 + df["buy_hold_return"]).cumprod()
    df["buy_hold_value"] = initial_capital * df["buy_hold_equity"]

    metrics = calculate_metrics(df)

    return df, metrics
