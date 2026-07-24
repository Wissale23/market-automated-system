# Real-Time Market Data Pipeline & Trading Strategy Engine

## Overview

This project is a modular quantitative trading system that ingests real market data, engineers financial features, generates trading signals, manages portfolio risk, and evaluates strategy performance through historical backtesting.

The system simulates a realistic quantitative trading workflow including:

- Market data ingestion
- Feature engineering
- Trading signal generation
- Risk management
- Portfolio simulation
- Performance analytics
- Benchmark comparison against Buy & Hold

The goal is to build a production-style algorithmic trading pipeline using Python.

---

# System Architecture


---

## Features

### Data Ingestion
- Real-time market data fetched using Yahoo Finance API (`yfinance`)
- Structured storage of OHLCV data
- Multi-asset ready design

### Feature Engineering
- Returns calculation
- Moving averages (MA5, MA20)
- Rolling volatility
- Momentum features

### Signal Generation
- Moving Average crossover strategy
- Buy/Sell/Hold signal generation
- Lookahead bias prevention (signal shifting)

###  Backtesting Engine
- Portfolio simulation with initial capital
- Transaction cost modelling
- Equity curve computation
- Buy & Hold benchmark comparison

### Performance Metrics
- Sharpe Ratio
- Maximum Drawdown
- Win Rate
- Total Strategy Return vs Market Return

##  Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib
- yfinance
