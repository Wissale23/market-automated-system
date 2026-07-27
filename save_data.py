from ingestion.fetch_data import fetch_stock_data, save_to_csv


tickers = [
    "AAPL",
    "MSFT",
    "GOOG",
    "META",
    "AMZN",
    "NVDA"
]


for symbol in tickers:
    df = fetch_stock_data(symbol)
    save_to_csv(df, symbol)

print("All data saved.")