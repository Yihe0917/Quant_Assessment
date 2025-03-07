import pandas as pd

def backtest(data, signals, initial_capital, min_trade_size):
    positions = pd.Series(0, index=data.index)  
    cash = initial_capital  
    portfolio_value = pd.Series(index=data.index, dtype='float64')  
    trades = []  

    for i, price in data.items():
        signal = signals.get(i, 0)  
        idx = data.index.get_loc(i)  

        prev_position = positions.iloc[idx - 1] if idx > 0 else 0

        if signal == 1:  
            shares_to_buy = int(cash / price)  
            shares_to_buy = max(shares_to_buy, min_trade_size)  
            cost = shares_to_buy * price

            if cash >= cost:
                positions.loc[i] = prev_position + shares_to_buy  
                cash -= cost
                trades.append({'date': i, 'action': 'buy', 'price': price, 'shares': shares_to_buy})
            else:
                positions.loc[i] = prev_position  

        elif signal == -1:  
            shares_to_sell = prev_position  
            if shares_to_sell > 0:
                revenue = shares_to_sell * price
                cash += revenue
                positions.loc[i] = 0  
                trades.append({'date': i, 'action': 'sell', 'price': price, 'shares': shares_to_sell})
            else:
                positions.loc[i] = prev_position  

        else:
            positions.loc[i] = prev_position  

        portfolio_value.loc[i] = cash + (positions.loc[i] * price)

    trades_df = pd.DataFrame(trades)
    return portfolio_value, trades_df
