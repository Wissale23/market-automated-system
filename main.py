from ingestion.fetch_data import fetch_stock_data
from features.feature_engineering import add_basic_features
from portfolio import portfolio
from signals.signal_engine import generate_signals
from backtest.backtest_engine import run_backtest
from utils.plot import plot_equity
from risk.risk_manager import apply_risk_management
from analytics.performance import calculate_performance
from utils.logger import setup_logger
import json
import os
from portfolio.portfolio import Portfolio
from portfolio.optimizer import (
    equal_weight,
    volatility_weight,
    minimum_variance,
    maximum_sharpe
)
from analytics.portfolio_performance import calculate_portfolio_metrics

from config.config import INITIAL_CAPITAL


def main():

    logger = setup_logger()

    tickers = [
        "AAPL",
        "MSFT",
        "GOOG",
        "META",
        "AMZN",
        "NVDA"
    ]

    results = {}

    for symbol in tickers:

        logger.info(f"Loading {symbol}")

        df = fetch_stock_data(symbol)

        print("\nColumns after ingestion:")
        print(df.columns.tolist())

        logger.info("Creating features")
        df = add_basic_features(df)

        logger.info("Generating signals")
        df = generate_signals(df)

        logger.info("Applying risk management")
        print("\nColumns before risk management:")
        print(df.columns.tolist())

        df = apply_risk_management(df)

        logger.info("Running backtest")
        df, metrics = run_backtest(df,initial_capital=10000,transaction_cost=0.001,slippage=0.0005)

        performance = calculate_performance(df)

        results[symbol] = {
            "data": df,
            "metrics": metrics,
            "performance": performance
        }

        close_col = f"close_{symbol.lower()}"

        print(f"\n===== {symbol} =====")

        print(
            df[
                [
                    close_col,
                    "signal",
                    "position",
                    "portfolio_value",
                    "buy_hold_value"
                ]
            ].tail()
        )

        print("\nMetrics:")
        print(metrics)

        print("\nPerformance:")
        print(performance)

        plot_equity(df,symbol)

    print("\nProcessed tickers:")
    print(results.keys())


    # -------------------------
    # Portfolio construction
    # -------------------------


        # Choose allocation model

    weights = maximum_sharpe(results)


    print("\nPORTFOLIO WEIGHTS")
    print("-----------------")

    for symbol, weight in weights.items():

        print(
            f"{symbol}: {weight:.2%}"
        )


    portfolio = Portfolio(
        initial_capital=INITIAL_CAPITAL
    )


    portfolio.allocate(weights)


    portfolio_curve = portfolio.calculate_equity_curve(results)

    final_value = portfolio_curve.iloc[-1]
    
    portfolio_metrics = calculate_portfolio_metrics(
        portfolio_curve
    )

    print("\nPORTFOLIO PERFORMANCE")
    print("---------------------")

    print(
        f"Initial capital: £{portfolio.initial_capital}"
    )

    print(
        f"Final value: £{final_value:.2f}"
    )

    print(
        f"Return: {(final_value / portfolio.initial_capital - 1):.2%}"
    )

    print("\nPORTFOLIO METRICS")
    print("-----------------")

    for key, value in portfolio_metrics.items():

        print(
            f"{key}: {value:.4f}"
        )

    #saving outputs
    
    os.makedirs("outputs/reports", exist_ok=True)

    for symbol, result in results.items():

        metrics = result["metrics"]

        metrics = {
            k: float(v)
            for k, v in metrics.items()
        }

        with open(
            f"outputs/reports/{symbol}_metrics.json",
            "w"
        ) as f:
            json.dump(metrics, f, indent=4)


if __name__ == "__main__":
    main()
    