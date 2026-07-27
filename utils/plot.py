import matplotlib.pyplot as plt
import os


def plot_equity(df, symbol):
    """
    Plot strategy performance against buy-and-hold benchmark.
    """

    plt.figure(figsize=(10, 5))

    plt.plot(
        df["portfolio_value"],
        label="Strategy"
    )

    plt.plot(
        df["buy_hold_value"],
        label="Buy & Hold"
    )

    plt.title(f"{symbol} Strategy vs Market Benchmark")
    plt.xlabel("Time")
    plt.ylabel("Portfolio Value")
    plt.legend()
    plt.grid(True)

    # Create output folder
    os.makedirs("outputs/plots", exist_ok=True)

    # Save figure
    plt.savefig(
        f"outputs/plots/{symbol}_equity.png",
        bbox_inches="tight"
    )

    plt.show()

    plt.close()