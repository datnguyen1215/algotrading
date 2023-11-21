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
    df.drop(['symbol'], axis=1, inplace=True)
    df = add_indicators(df)
    return df

def add_indicators(df):
    # include rsi 7 and sma of the rsi 7
    df['rsi_7'] = ta.momentum.rsi(df['close'], window=7)
    df['rsi_7_sma'] = ta.trend.sma_indicator(df['rsi_7'], window=7)
    
    # subtract rsi_7 and rsi_7_sma
    df['rsi_7_diff'] = df['rsi_7'] - df['rsi_7_sma']
    
    # include rsi 14 and sma 14 of the rsi
    df['rsi_14'] = ta.momentum.rsi(df['close'], window=14)
    df['rsi_14_sma'] = ta.trend.sma_indicator(df['rsi_14'], window=14)
    
    # subtract rsi_14 and rsi_14_sma
    df['rsi_14_diff'] = df['rsi_14'] - df['rsi_14_sma']
    
    # include atr rma
    df['atr'] = ta.volatility.average_true_range(df['high'], df['low'], df['close'], window=14, fillna=True)
    
    # include ema 3
    df['ema_3'] = ta.trend.ema_indicator(df['close'], window=3)

    # include ema 5
    df['ema_5'] = ta.trend.ema_indicator(df['close'], window=5)

    # include ema 8
    df['ema_8'] = ta.trend.ema_indicator(df['close'], window=8)

    # include ema 13
    df['ema_13'] = ta.trend.ema_indicator(df['close'], window=13)

    # include ema 21
    df['ema_21'] = ta.trend.ema_indicator(df['close'], window=21)
    
    # diff ema 3
    df['ema_3_5_diff'] = df['ema_3'] - df['ema_5']
    df['ema_3_8_diff'] = df['ema_3'] - df['ema_8']
    df['ema_3_13_diff'] = df['ema_3'] - df['ema_13']
    df['ema_3_21_diff'] = df['ema_3'] - df['ema_21']
    
    # diff ema 5
    df['ema_5_8_diff'] = df['ema_5'] - df['ema_8']
    df['ema_5_13_diff'] = df['ema_5'] - df['ema_13']
    df['ema_5_21_diff'] = df['ema_5'] - df['ema_21']

    # diff ema 8
    df['ema_8_13_diff'] = df['ema_8'] - df['ema_13']
    df['ema_8_21_diff'] = df['ema_8'] - df['ema_21']

    # diff ema 13
    df['ema_13_21_diff'] = df['ema_13'] - df['ema_21']
    
    # include MACD 6 3 5
    df['macd_6_3'] = ta.trend.macd_diff(df['close'], window_slow=6, window_fast=3, window_sign=5, fillna=True)
    df['macd_6_3_ema'] = ta.trend.ema_indicator(df['macd_6_3'], window=5)
    df['macd_6_3_diff'] = df['macd_6_3'] - df['macd_6_3_ema']
    
    # include MACD 12 26 9
    df['macd_12_26'] = ta.trend.macd_diff(df['close'], window_slow=26, window_fast=12, window_sign=9, fillna=True)
    df['macd_12_26_ema'] = ta.trend.ema_indicator(df['macd_12_26'], window=9)
    df['macd_12_26_diff'] = df['macd_12_26'] - df['macd_12_26_ema']
    
    # include stochastic 5 5 3
    df['stoch_5_5_k'] = ta.momentum.stoch(df['high'], df['low'], df['close'], window=5, smooth_window=5, fillna=True)
    df['stoch_5_5_d'] = ta.trend.sma_indicator(df['stoch_5_5_k'], window=3)
    df['stoch_5_5_diff'] = df['stoch_5_5_k'] - df['stoch_5_5_d']
    
    # include stochastic 10 10 6
    df['stoch_10_10_k'] = ta.momentum.stoch(df['high'], df['low'], df['close'], window=10, smooth_window=10, fillna=True)
    df['stoch_10_10_d'] = ta.trend.sma_indicator(df['stoch_10_10_k'], window=6)
    df['stoch_10_10_diff'] = df['stoch_10_10_k'] - df['stoch_10_10_d']
    
    # ichimoku cloud
    df['ichimoku_a'] = ta.trend.ichimoku_a(df['high'], df['low'], window1=9, window2=26, visual=False, fillna=True)
    df['ichimoku_b'] = ta.trend.ichimoku_b(df['high'], df['low'], window2=52, window3=26, visual=False, fillna=True)
    df['ichimoku_a_b_diff'] = df['ichimoku_a'] - df['ichimoku_b']

    # Directional Indicator Plus 14
    df['di_plus'] = ta.trend.adx_pos(df['high'], df['low'], df['close'], window=14, fillna=True)
    df['di_minus'] = ta.trend.adx_neg(df['high'], df['low'], df['close'], window=14, fillna=True)
    df['di_diff'] = df['di_plus'] - df['di_minus']
    
    # upper boilinger band 7 2
    df['bb_upper_7_2'] = ta.volatility.bollinger_hband(df['close'], window=7, window_dev=2, fillna=True)
    df['bb_lower_7_2'] = ta.volatility.bollinger_lband(df['close'], window=7, window_dev=2, fillna=True)
    df['bb_7_2_diff'] = df['bb_upper_7_2'] - df['bb_lower_7_2']
    
    # upper boilinger band 20 2
    df['bb_upper_20_2'] = ta.volatility.bollinger_hband(df['close'], window=20, window_dev=2, fillna=True)
    df['bb_lower_20_2'] = ta.volatility.bollinger_lband(df['close'], window=20, window_dev=2, fillna=True)
    df['bb_20_2_diff'] = df['bb_upper_20_2'] - df['bb_lower_20_2']

    # drop rows that contain NaN
    df.dropna(inplace=True)

    return df

# resample df to timeframej
def resample_df(df, timeframe):
    new_df = df.resample(timeframe).agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'})
    new_df = add_indicators(new_df)
    return new_df

# plot candles
def plot(df):
    df['close'].plot(figsize=(12, 8), title=df['symbol'][0], grid=True)
    plt.show()
