# Real-Time Market Data Pipeline & Trading Strategy Engine

## Overview

This project is a modular trading system that ingests real market data, engineers financial features, generates trading signals, and evaluates strategy performance using backtesting and benchmark comparison against a Buy & Hold strategy.

The goal is to simulate a realistic quantitative trading workflow with proper risk metrics, transaction costs, and performance evaluation.

---

## System Architecture

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
