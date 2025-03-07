import numpy as np
import pandas as pd

def calculate_performance_metrics(portfolio_values, risk_free_rate):
    returns = portfolio_values.pct_change().dropna()

    if returns.empty or portfolio_values.isna().all():
        return {
            "total_return": 0, "annualized_return": 0, "annualized_volatility": 0,
            "sharpe_ratio": 0, "sortino_ratio": 0, "max_drawdown": 0, "calmar_ratio": 0
        }

    initial_value = portfolio_values.iloc[0]
    final_value = portfolio_values.iloc[-1]

    total_return = (final_value - initial_value) / initial_value
    num_days = len(portfolio_values)
    annualized_return = (final_value / initial_value) ** (252 / num_days) - 1 if num_days > 0 else 0
    annualized_volatility = returns.std() * np.sqrt(252) if returns.std() != 0 else 0

    excess_returns = returns - (risk_free_rate / 252)  
    sharpe_ratio = excess_returns.mean() / annualized_volatility if annualized_volatility != 0 else 0

    downside_returns = returns[returns < 0]
    downside_volatility = downside_returns.std() * np.sqrt(252) if not downside_returns.empty else 0
    sortino_ratio = excess_returns.mean() / downside_volatility if downside_volatility != 0 else 0

    rolling_max = portfolio_values.cummax()  
    drawdown = (portfolio_values - rolling_max) / rolling_max  
    max_drawdown = drawdown.min() if not drawdown.isna().all() else 0  

    calmar_ratio = annualized_return / abs(max_drawdown) if max_drawdown != 0 else 0

    metrics = {
        "total_return": total_return,
        "annualized_return": annualized_return,
        "annualized_volatility": annualized_volatility,
        "sharpe_ratio": sharpe_ratio,
        "sortino_ratio": sortino_ratio,
        "max_drawdown": max_drawdown,
        "calmar_ratio": calmar_ratio
    }

    return metrics
