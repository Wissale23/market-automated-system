import yfinance as yf
import pandas as pd
import streamlit as st


@st.cache_data(ttl=3600)
def fetch_stock_data(
    symbol: str,
    period: str = "6mo",
    interval: str = "1d"
):
    """
    Fetch historical stock data from Yahoo Finance.
    """

    print(f"Fetching data for {symbol}...")


    data = yf.download(
        symbol,
        period=period,
        interval=interval
    )


    if data.empty:
        raise ValueError(
            f"No data returned for {symbol}"
        )


    data.reset_index(inplace=True)


    data.columns = [
        "_".join(col).lower()
        if isinstance(col, tuple)
        else col.lower()
        for col in data.columns
    ]


    data["symbol"] = symbol


    print(
        f"Fetched {len(data)} rows for {symbol}"
    )


    return data