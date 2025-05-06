import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import yfinance as yf
from datetime import datetime, timedelta


class PortfolioOptimizer:
    def __init__(self, tickers=None, start_date=None, end_date=None):
        if tickers is None:
            self.tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'BRK-B']
        else:
            self.tickers = tickers

        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=3 * 365)).strftime('%Y-%m-%d')

        self.start_date = start_date
        self.end_date = end_date
        self.returns = None
        self.mean_returns = None
        self.cov_matrix = None
        self.num_assets = len(self.tickers)

    def fetch_data(self):
        try:
            data = yf.download(self.tickers, start=self.start_date, end=self.end_date)
            if data.empty:
                print("No data retrieved from Yahoo Finance")
                return False

            print("Data keys:", data.keys())  # Debugging line to inspect data structure

            if ('Close', self.tickers[0]) not in data.columns:
                print("Close prices not found in the data")
                return False

            # Extract 'Close' prices for all tickers
            close_prices = data['Close']
            if close_prices.empty:
                print("No Close prices available")
                return False

            self.returns = close_prices.pct_change().dropna()
            self.mean_returns = self.returns.mean()
            self.cov_matrix = self.returns.cov()
            return True
        except Exception as e:
            print(f"Error fetching data: {e}")
            return False

    def portfolio_performance(self, weights):
        returns = np.sum(self.mean_returns * weights) * 252
        volatility = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix * 252, weights)))
        return returns, volatility

    def negative_sharpe_ratio(self, weights, risk_free_rate=0.02):
        returns, volatility = self.portfolio_performance(weights)
        sharpe_ratio = (returns - risk_free_rate) / volatility
        return -sharpe_ratio

    def optimize_portfolio(self, risk_free_rate=0.02, constraint_set=None):
        if self.returns is None:
            success = self.fetch_data()
            if not success:
                return None

        init_weights = np.array([1.0 / self.num_assets] * self.num_assets)

        if constraint_set == 'long_only':
            bounds = tuple((0, 1) for _ in range(self.num_assets))
        elif constraint_set == 'long_short':
            bounds = tuple((-1, 1) for _ in range(self.num_assets))
        else:
            bounds = tuple((0, 1) for _ in range(self.num_assets))

        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

        result = minimize(
            self.negative_sharpe_ratio,
            init_weights,
            args=(risk_free_rate,),
            method='SLSQP',
            bounds=bounds,
            constraints=constraints,
            options={'disp': False}
        )

        optimal_weights = result['x']
        returns, volatility = self.portfolio_performance(optimal_weights)
        sharpe_ratio = (returns - risk_free_rate) / volatility

        results = {
            'weights': dict(zip(self.tickers, np.round(optimal_weights, 4))),
            'expected_annual_return': returns,
            'annual_volatility': volatility,
            'sharpe_ratio': sharpe_ratio
        }

        return results

    def efficient_frontier(self, num_portfolios=1000):
        if self.returns is None:
            success = self.fetch_data()
            if not success:
                return None

        results = []

        for _ in range(num_portfolios):
            weights = np.random.random(self.num_assets)
            weights /= np.sum(weights)
            returns, volatility = self.portfolio_performance(weights)
            results.append([returns, volatility, *weights])

        results_df = pd.DataFrame(results, columns=['returns', 'volatility', *self.tickers])
        return results_df

    def plot_efficient_frontier(self, num_portfolios=1000, risk_free_rate=0.02):
        if self.returns is None:
            success = self.fetch_data()
            if not success:
                return

        results_df = self.efficient_frontier(num_portfolios)
        optimal_portfolio = self.optimize_portfolio(risk_free_rate)

        plt.figure(figsize=(10, 6))
        plt.scatter(results_df['volatility'], results_df['returns'], c=results_df['returns'] / results_df['volatility'],
                    cmap='viridis', alpha=0.6, s=10)
        plt.colorbar(label='Sharpe Ratio')

        plt.scatter(optimal_portfolio['annual_volatility'], optimal_portfolio['expected_annual_return'],
                    c='red', s=100, edgecolors='black', marker='*')

        plt.xlabel('Volatility (Standard Deviation)')
        plt.ylabel('Expected Return')
        plt.title('Efficient Frontier with Optimal Portfolio')
        plt.grid(True, linestyle='-', alpha=0.2)

        return plt


if __name__ == "__main__":
    optimizer = PortfolioOptimizer()
    result = optimizer.optimize_portfolio()

    if result is None:
        print("Portfolio optimization failed. Please check the data and try again.")
    else:
        print("Optimal Portfolio Weights:", result['weights'])
        print(f"Expected Annual Return: {result['expected_annual_return']:.4f}")
        print(f"Annual Volatility: {result['annual_volatility']:.4f}")
        print(f"Sharpe Ratio: {result['sharpe_ratio']:.4f}")

        plt = optimizer.plot_efficient_frontier()
        plt.show()