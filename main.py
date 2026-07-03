from ingestion.fetch_data import fetch_stock_data
from features.feature_engineering import add_basic_features
from signals.signal_engine import generate_signals
from backtest.backtest_engine import run_backtest
from utils.plot import plot_equity



def main():
    symbol = "AAPL"

    df = fetch_stock_data(symbol)
    df = add_basic_features(df)
    df = generate_signals(df)

    df, metrics = run_backtest(df)

    print("\nFINAL RESULTS:")
    print(df[["close_aapl", "signal", "portfolio_value", "buy_hold_value"]].tail())

    print("\nMETRICS:")
    print(metrics)
    plot_equity(df)


if __name__ == "__main__":
    main()
    
from utils.plot import plot_equity

