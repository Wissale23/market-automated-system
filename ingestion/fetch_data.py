import yfinance as yf
import pandas as pd
from datetime import datetime

def fetch_stock_data(symbol: str, period: str = "6mo", interval: str = "1d"):
    """
    Fetch historical stock data from Yahoo Finance.
    """

    print(f"Fetching data for {symbol}...")

    data = yf.download(symbol, period=period, interval=interval)

    if data.empty:
        raise ValueError(f"No data returned for {symbol}")

    # Clean column names
    data.reset_index(inplace=True)
    # Clean column names safely (handles strings + tuples)
    data.columns = [
        "_".join(col).lower() if isinstance(col, tuple) else col.lower()
        for col in data.columns
]

    # Add symbol column (important for later multi-asset support)
    data["symbol"] = symbol

    print(f"Fetched {len(data)} rows for {symbol}")

    return data


def save_to_csv(df: pd.DataFrame, symbol: str):
    """
    Save data locally for now (we'll upgrade to PostgreSQL later).
    """

    filename = f"data/{symbol}_data.csv"
    df.to_csv(filename, index=False)

    print(f"Saved data to {filename}")


if __name__ == "__main__":
    symbol = "AAPL"

    df = fetch_stock_data(symbol)
    save_to_csv(df, symbol)

    print("Done.")