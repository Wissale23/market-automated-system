class Portfolio:

    def __init__(self, initial_capital=10000):

        self.initial_capital = initial_capital
        self.weights = {}
        

    def allocate(self, weights):

        self.weights = weights


    def calculate_equity_curve(self, results):
        """
        Calculate daily portfolio value.
        """

        portfolio_returns = None

        for symbol, weight in self.weights.items():

            df = results[symbol]["data"]

            weighted_returns = (
                df["returns"] * weight
            )

            if portfolio_returns is None:
                portfolio_returns = weighted_returns

            else:
                portfolio_returns += weighted_returns


        equity_curve = (
            1 + portfolio_returns
        ).cumprod() * self.initial_capital


        return equity_curve