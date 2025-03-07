import pandas as pd
import numpy as np

def calculate_bollinger_bands(data, period, std_dev_mult):
    rolling_mean = data.rolling(window=period).mean()
    rolling_std = data.rolling(window=period).std()

    upper_band = rolling_mean + (rolling_std * std_dev_mult)
    lower_band = rolling_mean - (rolling_std * std_dev_mult)

    return pd.DataFrame({'Upper': upper_band, 'Lower': lower_band, 'Moving Average': rolling_mean})

def generate_trading_signals(data, upper_band, lower_band):
    signals = pd.Series(0, index=data.index)

    signals[data > upper_band] = 1
    signals[data < lower_band] = -1

    signals = signals.replace(0, np.nan).ffill().fillna(0)
    signals = signals[signals.shift() != signals]

    return signals
