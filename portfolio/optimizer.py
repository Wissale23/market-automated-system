import numpy as np
import pandas as pd


def equal_weight(symbols):
    """
    Allocate equal capital to every asset.
    """

    n = len(symbols)

    return {
        symbol: 1/n
        for symbol in symbols
    }



def volatility_weight(results):
    """
    Allocate more capital to less volatile assets.
    """

    volatilities = {}

    for symbol, result in results.items():

        df = result["data"]

        volatility = df["returns"].std()

        volatilities[symbol] = volatility


    inverse_vol = {
        symbol: 1/vol
        for symbol, vol in volatilities.items()
    }


    total = sum(inverse_vol.values())


    weights = {
        symbol: value / total
        for symbol, value in inverse_vol.items()
    }


    return weights



def minimum_variance(results):
    """
    Simple minimum variance approximation.
    Uses inverse volatility weighting.
    """

    return volatility_weight(results)


def maximum_sharpe(results, max_weight=0.4):

    sharpes = {}

    for symbol, result in results.items():

        sharpe = result["metrics"]["sharpe_ratio"]

        sharpes[symbol] = max(sharpe, 0)


    total = sum(sharpes.values())


    if total == 0:
        return equal_weight(list(results.keys()))


    weights = {
        symbol: value / total
        for symbol, value in sharpes.items()
    }


    # Apply maximum weight constraint

    for symbol in weights:

        if weights[symbol] > max_weight:
            weights[symbol] = max_weight


    # Renormalise remaining weights

    total_weight = sum(weights.values())

    weights = {
        symbol: weight / total_weight
        for symbol, weight in weights.items()
    }


    return weights