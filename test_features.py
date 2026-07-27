from ingestion.fetch_data import fetch_stock_data
from features.feature_engineering import add_basic_features
from signals.signal_engine import generate_signals
from backtest.backtest_engine import run_backtest

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

    print(f"\nRunning {symbol}...")

    df = fetch_stock_data(symbol)
    df = add_basic_features(df)
    df = generate_signals(df)
    df = run_backtest(df)

    results[symbol] = df

    print(df.tail())