import pandas as pd
from data_fetch import get_stock_data
from bollinger import calculate_bollinger_bands, generate_trading_signals
from backtest import backtest
from performance import calculate_performance_metrics

tickers = ['MSFT', 'AAPL', 'NVDA', 'AMZN', 'GOOG', 'META', 'TSLA']
start_date = '2013-01-01'
end_date = '2023-12-31'
initial_capital = 10000
min_trade_size = 1
risk_free_rate = 0.02

all_metrics = {}
all_portfolios = {}
all_trades = {}

portfolio_values = pd.DataFrame()

for ticker in tickers:
    print(f"Processing {ticker}...")

    stock_data = get_stock_data([ticker], start_date, end_date)
    data = stock_data[ticker]
    
    bollinger_bands = calculate_bollinger_bands(data, period=20, std_dev_mult=2)
    signals = generate_trading_signals(data, bollinger_bands['Upper'], bollinger_bands['Lower'])

    portfolio_value, trades = backtest(data, signals, initial_capital, min_trade_size)

    stock_metrics = calculate_performance_metrics(portfolio_value, risk_free_rate)
    all_metrics[ticker] = stock_metrics
    all_portfolios[ticker] = portfolio_value
    all_trades[ticker] = trades

    portfolio_values[ticker] = portfolio_value

if not portfolio_values.empty:
    total_portfolio_value = portfolio_values.sum(axis=1)
    portfolio_metrics = calculate_performance_metrics(total_portfolio_value, risk_free_rate)
else:
    total_portfolio_value = pd.Series(dtype=float)
    portfolio_metrics = {}

# Print out metrics
print("\nIndividual Stock Metrics:")
for ticker, metric in all_metrics.items():
    print(f"{ticker}: {metric}")

print("\nTotal Portfolio Metrics:")
print(portfolio_metrics)
