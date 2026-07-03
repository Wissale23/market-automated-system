import matplotlib.pyplot as plt


def plot_equity(df):
    plt.figure(figsize=(10,5))

    plt.plot(df["portfolio_value"], label="Strategy")
    plt.plot(df["buy_hold_value"], label="Buy & Hold")

    plt.title("Strategy vs Market Benchmark")
    plt.xlabel("Time")
    plt.ylabel("Portfolio Value")
    plt.legend()
    plt.grid(True)

    plt.show()