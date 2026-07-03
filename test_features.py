from ingestion.fetch_data import fetch_stock_data
from features.feature_engineering import add_basic_features
from signals.signal_engine import generate_signals
from backtest.backtest_engine import run_backtest

symbol = "AAPL"

df = fetch_stock_data(symbol)
df = add_basic_features(df)
df = generate_signals(df)
df = run_backtest(df)

print(df[["close_aapl", "signal", "portfolio_value"]].tail())