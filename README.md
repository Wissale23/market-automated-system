# 📊 Real-Time Market Data Pipeline & Trading Strategy Engine

## 🧠 Overview

This project is a modular trading system that ingests real market data, engineers financial features, generates trading signals, and evaluates strategy performance using backtesting and benchmark comparison against a Buy & Hold strategy.

The goal is to simulate a realistic quantitative trading workflow with proper risk metrics, transaction costs, and performance evaluation.

---

## ⚙️ System Architecture

---

## 🚀 Features

### 📥 Data Ingestion
- Real-time market data fetched using Yahoo Finance API (`yfinance`)
- Structured storage of OHLCV data
- Multi-asset ready design

### ⚙️ Feature Engineering
- Returns calculation
- Moving averages (MA5, MA20)
- Rolling volatility
- Momentum features

### 📊 Signal Generation
- Moving Average crossover strategy
- Buy/Sell/Hold signal generation
- Lookahead bias prevention (signal shifting)

### 📉 Backtesting Engine
- Portfolio simulation with initial capital
- Transaction cost modelling
- Equity curve computation
- Buy & Hold benchmark comparison

### 📈 Performance Metrics
- Sharpe Ratio
- Maximum Drawdown
- Win Rate
- Total Strategy Return vs Market Return

---

## 📊 Example Results

| Metric | Value |
|--------|------|
| Sharpe Ratio | -0.49 |
| Max Drawdown | -15.5% |
| Win Rate | 46.6% |
| Strategy Return | Negative / variable |
| Buy & Hold Return | Market benchmark |

---

## 📉 Key Insight

The current simple moving average crossover strategy underperforms the market, highlighting the importance of:
- better signal filtering
- regime detection
- risk management

This project is designed as a **research and experimentation framework**, not a production trading system.

---

## 🧠 What This Demonstrates

- Data engineering (pipeline design)
- Financial modelling (returns, risk metrics)
- Algorithmic thinking (signal generation)
- System design (modular architecture)
- Evaluation mindset (benchmarking vs market)

---

## 🛠️ Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib
- yfinance

---

## 📊 Visual Output

- Strategy vs Buy & Hold equity curve
- Performance metrics comparison

---

## 🚀 Future Improvements

- Walk-forward validation
- Multi-asset portfolio simulation
- Advanced risk models (Sortino, VaR)
- ML-based signal generation
- Live data streaming pipeline

---

## 📌 How to Run

```bash
python main.py
