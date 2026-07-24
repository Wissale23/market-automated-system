from ingestion.fetch_data import fetch_stock_data
from features.feature_engineering import add_basic_features
from signals.signal_engine import generate_signals
from backtest.backtest_engine import run_backtest
from utils.plot import plot_equity
from risk.risk_manager import apply_risk_management
from analytics.performance import calculate_performance
from utils.logger import setup_logger


def main():

    logger = setup_logger()

    symbol = "AAPL"

    logger.info("Loading data")

    df = fetch_stock_data(symbol)

    logger.info("Creating features")

    df = add_basic_features(df)

    logger.info("Generating signals")

    df = generate_signals(df)


    logger.info("Applying risk management")

    df = apply_risk_management(df)


    logger.info("Running backtest")

    df, metrics = run_backtest(df)


    performance = calculate_performance(df)


    print("\nFINAL RESULTS:")
    print(
        df[
            [
                "close_aapl",
                "signal",
                "position",
                "portfolio_value",
                "buy_hold_value"
            ]
        ].tail()
    )


    print("\nBACKTEST METRICS:")
    print(metrics)


    print("\nPERFORMANCE:")
    print(performance)


    plot_equity(df)


if __name__ == "__main__":
    main()
    
from utils.plot import plot_equity

