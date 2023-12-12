# get candles from http://localhost:3005/api/candles

import requests
import pandas as pd
import matplotlib.pyplot as plt
import ta
import math
import numpy as np
from sklearn.preprocessing import MinMaxScaler


# get candles from http://localhost:3005/api/candles
def get(symbol, n_candles=5000):
    url = f"http://localhost:3005/api/candles?limit={n_candles}&filter[symbol]={symbol}"
    r = requests.get(url)
    candles = r.json()
    return candles_to_df(candles)


# convert candles to pandas dataframe
def candles_to_df(candles):
    df = pd.DataFrame(candles)
    df["time"] = pd.to_datetime(df["time"])
    df.set_index("time", inplace=True)
    df.drop(["symbol"], axis=1, inplace=True)
    return df


def get_angles(series, delta_x=5):
    diff = series.shift(-1) - series
    slopes = diff / delta_x
    return np.degrees(np.arctan(slopes))


def add_indicators(df, delta_x=5):
    # include rsi 7 and sma of the rsi 7
    rsi_7 = ta.momentum.rsi(df["close"], window=7)
    rsi_7_sma = ta.trend.sma_indicator(rsi_7, window=7)

    df["rsi_7_slope_angle"] = get_angles(rsi_7, delta_x)
    df["rsi_7_sma_slope_angle"] = get_angles(rsi_7_sma, delta_x)

    df["rsi_7_slope_angle_2"] = df["rsi_7_slope_angle"].shift()
    df["rsi_7_sma_slope_angle_2"] = df["rsi_7_slope_angle"].shift()

    df["rsi_7_slope_angle_3"] = df["rsi_7_slope_angle"].shift(2)
    df["rsi_7_sma_slope_angle_3"] = df["rsi_7_slope_angle"].shift(2)

    # include rsi 14 and sma 14 of the rsi
    rsi_14 = ta.momentum.rsi(df["close"], window=14)
    rsi_14_sma = ta.trend.sma_indicator(rsi_14, window=14)

    df["rsi_14_slope_angle"] = get_angles(rsi_14, delta_x)
    df["rsi_14_sma_slope_angle"] = get_angles(rsi_14_sma, delta_x)

    df["rsi_14_slope_angle_2"] = df["rsi_14_slope_angle"].shift()
    df["rsi_14_sma_slope_angle_2"] = df["rsi_14_slope_angle"].shift()

    df["rsi_14_slope_angle_3"] = df["rsi_14_slope_angle"].shift(2)
    df["rsi_14_sma_slope_angle_3"] = df["rsi_14_slope_angle"].shift(2)

    # include atr rma
    df["atr"] = ta.volatility.average_true_range(
        df["high"], df["low"], df["close"], window=14, fillna=True
    )

    # include ema 3
    ema_3 = ta.trend.ema_indicator(df["close"], window=3)
    ema_5 = ta.trend.ema_indicator(df["close"], window=5)
    ema_8 = ta.trend.ema_indicator(df["close"], window=8)
    ema_13 = ta.trend.ema_indicator(df["close"], window=13)
    ema_21 = ta.trend.ema_indicator(df["close"], window=21)

    df["avg_ema_3_slope_angle"] = get_angles(ema_3, delta_x)
    df["avg_ema_5_slope_angle"] = get_angles(ema_5, delta_x)
    df["avg_ema_8_slope_angle"] = get_angles(ema_8, delta_x)
    df["avg_ema_13_slope_angle"] = get_angles(ema_13, delta_x)
    df["avg_ema_21_slope_angle"] = get_angles(ema_21, delta_x)

    df["avg_ema_3_slope_angle_2"] = df["avg_ema_3_slope_angle"].shift()
    df["avg_ema_5_slope_angle_2"] = df["avg_ema_5_slope_angle"].shift()
    df["avg_ema_8_slope_angle_2"] = df["avg_ema_8_slope_angle"].shift()
    df["avg_ema_13_slope_angle_2"] = df["avg_ema_13_slope_angle"].shift()
    df["avg_ema_21_slope_angle_2"] = df["avg_ema_21_slope_angle"].shift()

    df["avg_ema_3_slope_angle_3"] = df["avg_ema_3_slope_angle"].shift(2)
    df["avg_ema_5_slope_angle_3"] = df["avg_ema_5_slope_angle"].shift(2)
    df["avg_ema_8_slope_angle_3"] = df["avg_ema_8_slope_angle"].shift(2)
    df["avg_ema_13_slope_angle_3"] = df["avg_ema_13_slope_angle"].shift(2)
    df["avg_ema_21_slope_angle_3"] = df["avg_ema_21_slope_angle"].shift(2)

    # include MACD 6 3 5
    macd_6_13 = ta.trend.macd_diff(
        df["close"], window_slow=13, window_fast=16, window_sign=5, fillna=True
    )
    macd_6_13_ema = ta.trend.ema_indicator(macd_6_13, window=5)

    df["macd_6_13_slope_angle"] = get_angles(macd_6_13, delta_x)
    df["macd_6_13_ema_slope_angle"] = get_angles(macd_6_13_ema, delta_x)

    df["macd_6_13_slope_angle_2"] = df["macd_6_13_slope_angle"].shift()
    df["macd_6_13_ema_slope_angle_2"] = df["macd_6_13_ema_slope_angle"].shift()

    df["macd_6_13_slope_angle_3"] = df["macd_6_13_slope_angle"].shift(2)
    df["macd_6_13_ema_slope_angle_3"] = df["macd_6_13_ema_slope_angle"].shift(2)

    # include MACD 12 26 9
    macd_12_26 = ta.trend.macd_diff(
        df["close"], window_slow=26, window_fast=12, window_sign=9, fillna=True
    )
    macd_12_26_ema = ta.trend.ema_indicator(macd_12_26, window=9)

    df["macd_12_26_slope_angle"] = get_angles(macd_12_26, delta_x)
    df["macd_12_26_ema_slope_angle"] = get_angles(macd_12_26_ema, delta_x)

    df["macd_12_26_slope_angle_2"] = df["macd_12_26_slope_angle"].shift()
    df["macd_12_26_ema_slope_angle_2"] = df["macd_12_26_ema_slope_angle"].shift()

    df["macd_12_26_slope_angle_3"] = df["macd_12_26_slope_angle"].shift(2)
    df["macd_12_26_ema_slope_angle_3"] = df["macd_12_26_ema_slope_angle"].shift(2)

    # include stochastic 5 5 3
    stoch_5_5_k = ta.momentum.stoch(
        df["high"], df["low"], df["close"], window=5, smooth_window=5, fillna=True
    )
    stoch_5_5_d = ta.trend.sma_indicator(stoch_5_5_k, window=3)

    df["stoch_5_5_k_slope_angle"] = get_angles(stoch_5_5_k, delta_x)
    df["stoch_5_5_d_slope_angle"] = get_angles(stoch_5_5_d, delta_x)

    df["stoch_5_5_k_slope_angle_2"] = df["stoch_5_5_k_slope_angle"].shift()
    df["stoch_5_5_d_slope_angle_2"] = df["stoch_5_5_d_slope_angle"].shift()

    df["stoch_5_5_k_slope_angle_3"] = df["stoch_5_5_k_slope_angle"].shift(2)
    df["stoch_5_5_d_slope_angle_3"] = df["stoch_5_5_d_slope_angle"].shift(2)

    # include stochastic 10 10 6
    stoch_10_10_k = ta.momentum.stoch(
        df["high"], df["low"], df["close"], window=10, smooth_window=10, fillna=True
    )
    stoch_10_10_d = ta.trend.sma_indicator(stoch_10_10_k, window=6)

    df["stoch_10_10_k_slope_angle"] = get_angles(stoch_10_10_k, delta_x)
    df["stoch_10_10_d_slope_angle"] = get_angles(stoch_10_10_d, delta_x)

    df["stoch_10_10_k_slope_angle_2"] = df["stoch_10_10_k_slope_angle"].shift()
    df["stoch_10_10_d_slope_angle_2"] = df["stoch_10_10_d_slope_angle"].shift()

    df["stoch_10_10_k_slope_angle_3"] = df["stoch_10_10_k_slope_angle"].shift(2)
    df["stoch_10_10_d_slope_angle_3"] = df["stoch_10_10_d_slope_angle"].shift(2)

    # Directional Indicator Plus 14
    di_plus = ta.trend.adx_pos(
        df["high"], df["low"], df["close"], window=7, fillna=True
    )
    di_minus = ta.trend.adx_neg(
        df["high"], df["low"], df["close"], window=7, fillna=True
    )

    df["di_plus_slope_angle"] = get_angles(di_plus, delta_x)
    df["di_minus_slope_angle"] = get_angles(di_minus, delta_x)

    df["di_plus_slope_angle_2"] = df["di_plus_slope_angle"].shift()
    df["di_minus_slope_angle_2"] = df["di_minus_slope_angle"].shift()

    df["di_plus_slope_angle_3"] = df["di_plus_slope_angle"].shift(2)
    df["di_minus_slope_angle_3"] = df["di_minus_slope_angle"].shift(2)

    # slope of the next candle
    df["next_close_slope_angle"] = get_angles(df["close"], delta_x)
    df["next_high_slope_angle"] = get_angles(df["high"], delta_x)
    df["next_low_slope_angle"] = get_angles(df["low"], delta_x)

    # filter prices that do not change
    close_changes = df["close"].shift(-1) - df["close"]
    high_changes = df["high"].shift(-1) - df["high"]
    low_changes = df["low"].shift(-1) - df["low"]

    df[(close_changes == 0) & (high_changes == 0) & (low_changes == 0)] = np.nan
    
    # use this for running simulation
    df['next_close'] = df['close'].shift(-1)
    df['next_high'] = df['high'].shift(-1)
    df['next_low'] = df['low'].shift(-1)

    df.dropna(inplace=True)

    return df


# remove outliers for multiple columns
def remove_outliers(df, columns):
    Q1 = df[columns].quantile(0.25)
    Q3 = df[columns].quantile(0.75)
    IQR = Q3 - Q1
    df = df[~((df[columns] < (Q1 - 1.5 * IQR)) | (df[columns] > (Q3 + 1.5 * IQR)))]
    return df


# resample df to timeframej
def resample_df(df, timeframe):
    new_df = df.resample(timeframe).agg(
        {"open": "first", "high": "max", "low": "min", "close": "last"}
    )
    return new_df


# plot candles
def plot(df):
    df["close"].plot(figsize=(12, 8), title=df["symbol"][0], grid=True)
    plt.show()
