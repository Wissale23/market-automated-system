from ingestion.fetch_data import fetch_stock_data
from features.feature_engineering import add_basic_features
from signals.signal_engine import generate_signals
from backtest.backtest_engine import run_backtest
from risk.risk_manager import apply_risk_management

from analytics.performance import calculate_performance
from analytics.portfolio_performance import calculate_portfolio_metrics

from portfolio.portfolio import Portfolio
from portfolio.optimizer import (
    equal_weight,
    volatility_weight,
    minimum_variance,
    maximum_sharpe
)

from utils.logger import setup_logger
from utils.plot import plot_equity

from config.config import (
    INITIAL_CAPITAL,
    MAX_POSITION,
    STOP_LOSS,
    TRANSACTION_COST
)


import json
import os


def run_pipeline(
    tickers,
    optimiser="maximum_sharpe",
    initial_capital=10000,
    ma_short=5,
    ma_long=20,
    stop_loss=0.05
):

    results = {}

    # -------------------------
    # Individual asset pipeline
    # -------------------------

    for symbol in tickers:

        df = fetch_stock_data(symbol)

        df = add_basic_features(
            df,
            ma_short=ma_short,
            ma_long=ma_long
        )

        df = generate_signals(
            df,
            ma_short=ma_short,
            ma_long=ma_long
        )

        df = apply_risk_management(
            df,
            max_position=MAX_POSITION,
            stop_loss=stop_loss
        )

        df, metrics = run_backtest(
            df,
            initial_capital=initial_capital,
            transaction_cost=TRANSACTION_COST,
            slippage=0.0005
        )

        performance = calculate_performance(df)


        results[symbol] = {
            "data": df,
            "metrics": metrics,
            "performance": performance
        }


    # -------------------------
    # Portfolio optimisation
    # -------------------------

    if optimiser == "equal_weight":

        weights = equal_weight(results)

    elif optimiser == "volatility_weight":

        weights = volatility_weight(results)

    elif optimiser == "minimum_variance":

        weights = minimum_variance(results)

    else:

        weights = maximum_sharpe(results)



    # -------------------------
    # Portfolio construction
    # -------------------------

    portfolio = Portfolio(
        initial_capital=initial_capital
    )

    portfolio.allocate(weights)


    portfolio_curve = portfolio.calculate_equity_curve(
        results
    )


    final_value = portfolio_curve.iloc[-1]


    portfolio_metrics = calculate_portfolio_metrics(
        portfolio_curve
    )


    return (
        results,
        weights,
        portfolio_curve,
        portfolio_metrics,
        final_value
    )



def save_reports(results):

    os.makedirs(
        "outputs/reports",
        exist_ok=True
    )


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

            json.dump(
                metrics,
                f,
                indent=4
            )



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


    logger.info("Starting trading pipeline")


    (
        results,
        weights,
        portfolio_curve,
        portfolio_metrics,
        final_value

    ) = run_pipeline(
        tickers=tickers,
        optimiser="maximum_sharpe",
        initial_capital=INITIAL_CAPITAL
    )



    # -------------------------
    # Print individual assets
    # -------------------------

    for symbol, result in results.items():

        df = result["data"]

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
        print(result["metrics"])


        print("\nPerformance:")
        print(result["performance"])


        plot_equity(
            df,
            symbol
        )



    # -------------------------
    # Portfolio results
    # -------------------------

    print("\nPORTFOLIO WEIGHTS")
    print("-----------------")


    for symbol, weight in weights.items():

        print(
            f"{symbol}: {weight:.2%}"
        )



    print("\nPORTFOLIO PERFORMANCE")
    print("---------------------")


    print(
        f"Initial capital: £{INITIAL_CAPITAL}"
    )


    print(
        f"Final value: £{final_value:.2f}"
    )


    print(
        f"Return: {(final_value / INITIAL_CAPITAL - 1):.2%}"
    )


    print("\nPORTFOLIO METRICS")
    print("-----------------")


    for key, value in portfolio_metrics.items():

        print(
            f"{key}: {value:.4f}"
        )



    save_reports(results)



if __name__ == "__main__":

    main()