# get candles from http://localhost:3005/api/candles

import requests
import pandas as pd
import matplotlib.pyplot as plt
import ta

# get candles from http://localhost:3005/api/candles
def get():
    url = "http://localhost:3005/api/candles?limit=10000&offset=3000"
    r = requests.get(url)
    candles = r.json()
    return candles_to_df(candles)

# convert candles to pandas dataframe
def candles_to_df(candles):
    df = pd.DataFrame(candles)
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)
    return df

# resample df to timeframej
def resample_df(df, timeframe):
    new_df = df.resample(timeframe).agg({'symbol': 'last', 'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'})
    new_df.reset_index(inplace=True)

    # include rsi 7 and sma of the rsi 7
    new_df['rsi_7'] = ta.momentum.rsi(new_df['close'], window=7)
    new_df['rsi_7_sma'] = ta.trend.sma_indicator(new_df['rsi_7'], window=7)
    
    # include rsi 14 and sma 14 of the rsi
    new_df['rsi_14'] = ta.momentum.rsi(new_df['close'], window=14)
    new_df['rsi_14_sma'] = ta.trend.sma_indicator(new_df['rsi_14'], window=14)
    
    # include atr rma
    new_df['atr'] = ta.volatility.average_true_range(new_df['high'], new_df['low'], new_df['close'], window=14, fillna=True)
    
    # include ema 3
    new_df['ema_3'] = ta.trend.ema_indicator(new_df['close'], window=3)

    # include ema 5
    new_df['ema_5'] = ta.trend.ema_indicator(new_df['close'], window=5)

    # include ema 8
    new_df['ema_8'] = ta.trend.ema_indicator(new_df['close'], window=8)

    # include ema 13
    new_df['ema_13'] = ta.trend.ema_indicator(new_df['close'], window=13)

    # include ema 21
    new_df['ema_21'] = ta.trend.ema_indicator(new_df['close'], window=21)
    
    # include MACD 6 3 with 5 EMA
    new_df['macd_6_3'] = ta.trend.macd_diff(new_df['close'], window_slow=6, window_fast=3, window_sign=5, fillna=True)
    
    # include MACD 12 26 with 9 EMA
    new_df['macd'] = ta.trend.macd_diff(new_df['close'], window_slow=26, window_fast=12, window_sign=9, fillna=True)
    
    # include stochastic 5 5
    new_df['stoch_5_5_k'] = ta.momentum.stoch(new_df['high'], new_df['low'], new_df['close'], window=5, smooth_window=5, fillna=True)
    
    # sma of stochastic 5 5
    new_df['stoch_5_5_d'] = ta.trend.sma_indicator(new_df['stoch_5_5_k'], window=3)
    
    # include stochastic 10 10
    new_df['stoch_10_10_k'] = ta.momentum.stoch(new_df['high'], new_df['low'], new_df['close'], window=10, smooth_window=10, fillna=True)
    
    # sma of stochastic 10 10, window = 6
    new_df['stoch_10_10_d'] = ta.trend.sma_indicator(new_df['stoch_10_10_k'], window=6)
    
    # ichimoku cloud
    new_df['ichimoku_a'] = ta.trend.ichimoku_a(new_df['high'], new_df['low'], window1=9, window2=26, visual=False, fillna=True)
    
    # ichimoku cloud leading span B 52
    new_df['ichimoku_b'] = ta.trend.ichimoku_b(new_df['high'], new_df['low'], window2=52, window3=26, visual=False, fillna=True)

    # Directional Indicator Plus 14
    new_df['di_plus'] = ta.trend.adx_pos(new_df['high'], new_df['low'], new_df['close'], window=14, fillna=True)
    
    # Directional Indicator Minus 14
    new_df['di_minus'] = ta.trend.adx_neg(new_df['high'], new_df['low'], new_df['close'], window=14, fillna=True)
    
    # upper boilinger band 7 2
    new_df['bb_upper_7_2'] = ta.volatility.bollinger_hband(new_df['close'], window=7, window_dev=2, fillna=True)
    
    # lower boilinger band 7 2
    new_df['bb_lower_7_2'] = ta.volatility.bollinger_lband(new_df['close'], window=7, window_dev=2, fillna=True)
    
    # upper boilinger band 20 2
    new_df['bb_upper_20_2'] = ta.volatility.bollinger_hband(new_df['close'], window=20, window_dev=2, fillna=True)

    # lower boilinger band 20 2
    new_df['bb_lower_20_2'] = ta.volatility.bollinger_lband(new_df['close'], window=20, window_dev=2, fillna=True)

    # drop rows that contain NaN
    new_df.dropna(inplace=True)

    return new_df

# plot candles
def plot(df):
    df['close'].plot(figsize=(12, 8), title=df['symbol'][0], grid=True)
    plt.show()
