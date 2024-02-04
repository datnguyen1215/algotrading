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
    slopes = series / delta_x
    return np.degrees(np.arctan(slopes))


def add_lookback(df, lookback=5):
    new_df = pd.DataFrame()

    for i in range(0, lookback):
        # for each column
        for column in df.columns:
            new_df[f"{column}_{i+2}"] = df[column].shift(i)

    return new_df



def add_indicators(df, delta_x=5):
    # include rsi 7 and sma of the rsi 7
    rsi_7 = ta.momentum.rsi(df["close"], window=7)
    rsi_7_sma = ta.trend.sma_indicator(rsi_7, window=7)
    rsi_7_close_sma_distance = rsi_7 - rsi_7_sma

    df["rsi_7_slope_angle"] = get_angles(rsi_7.diff(), delta_x)
    df['rsi_7_slope_angle_diff'] = rsi_7.diff()
    df['rsi_7_slope_angle_diff_angle'] = get_angles(rsi_7.diff(), delta_x)

    df["rsi_7_sma_slope_angle"] = get_angles(rsi_7_sma.diff(), delta_x)
    df['rsi_7_sma_slope_angle_diff'] = rsi_7_sma.diff()
    df['rsi_7_sma_slope_angle_diff_angle'] = get_angles(rsi_7_sma.diff(), delta_x)

    df['rsi_7_close_sma_distance_slope_angle'] = get_angles(rsi_7_close_sma_distance.diff(), delta_x)
    df['rsi_7_close_sma_distance_slope_angle_diff'] = rsi_7_close_sma_distance.diff()
    df['rsi_7_close_sma_distance_slope_angle_diff_angle'] = get_angles(rsi_7_close_sma_distance.diff(), delta_x)

    # include rsi 14 and sma 14 of the rsi
    rsi_14 = ta.momentum.rsi(df["close"], window=14)
    rsi_14_sma = ta.trend.sma_indicator(rsi_14, window=14)
    rsi_14_close_sma_distance = rsi_14 - rsi_14_sma

    df["rsi_14_slope_angle"] = get_angles(rsi_14.diff(), delta_x)
    df['rsi_14_slope_angle_diff'] = rsi_14.diff()
    df['rsi_14_slope_angle_diff_angle'] = get_angles(rsi_14.diff(), delta_x)

    df["rsi_14_sma_slope_angle"] = get_angles(rsi_14_sma.diff(), delta_x)
    df['rsi_14_sma_slope_angle_diff'] = rsi_14_sma.diff()
    df['rsi_14_sma_slope_angle_diff_angle'] = get_angles(rsi_14_sma.diff(), delta_x)

    df['rsi_14_close_sma_distance_slope_angle'] = get_angles(rsi_14_close_sma_distance.diff(), delta_x)
    df['rsi_14_close_sma_distance_slope_angle_diff'] = rsi_14_close_sma_distance.diff()
    df['rsi_14_close_sma_distance_slope_angle_diff_angle'] = get_angles(rsi_14_close_sma_distance.diff(), delta_x)


    # include ema 3
    ema_3 = ta.trend.ema_indicator(df["close"], window=3)
    ema_5 = ta.trend.ema_indicator(df["close"], window=5)
    ema_8 = ta.trend.ema_indicator(df["close"], window=8)
    ema_13 = ta.trend.ema_indicator(df["close"], window=13)
    ema_21 = ta.trend.ema_indicator(df["close"], window=21)

    df['ema_3_slope_angle'] = get_angles(ema_3.diff(), delta_x)
    df['ema_3_slope_angle_diff'] = ema_3.diff()
    df['ema_3_slope_angle_diff_angle'] = get_angles(ema_3.diff(), delta_x)

    df['ema_5_slope_angle'] = get_angles(ema_5.diff(), delta_x)
    df['ema_5_slope_angle_diff'] = ema_5.diff()
    df['ema_5_slope_angle_diff_angle'] = get_angles(ema_5.diff(), delta_x)

    df['ema_8_slope_angle'] = get_angles(ema_8.diff(), delta_x)
    df['ema_8_slope_angle_diff'] = ema_8.diff()
    df['ema_8_slope_angle_diff_angle'] = get_angles(ema_8.diff(), delta_x)

    df['ema_13_slope_angle'] = get_angles(ema_13.diff(), delta_x)
    df['ema_13_slope_angle_diff'] = ema_13.diff()
    df['ema_13_slope_angle_diff_angle'] = get_angles(ema_13.diff(), delta_x)

    df['ema_21_slope_angle'] = get_angles(ema_21.diff(), delta_x)
    df['ema_21_slope_angle_diff'] = ema_21.diff()
    df['ema_21_slope_angle_diff_angle'] = get_angles(ema_21.diff(), delta_x)

    ema_3_5_distance = ema_3 - ema_5
    ema_5_8_distance = ema_5 - ema_8
    ema_8_13_distance = ema_8 - ema_13
    ema_13_21_distance = ema_13 - ema_21

    df['ema_3_5_distance_slope_angle'] = get_angles(ema_3_5_distance.diff(), delta_x)
    df['ema_3_5_distance_slope_angle_diff'] = ema_3_5_distance.diff()
    df['ema_3_5_distance_slope_angle_diff_angle'] = get_angles(ema_3_5_distance.diff(), delta_x)

    df['ema_5_8_distance_slope_angle'] = get_angles(ema_5_8_distance.diff(), delta_x)
    df['ema_5_8_distance_slope_angle_diff'] = ema_5_8_distance.diff()
    df['ema_5_8_distance_slope_angle_diff_angle'] = get_angles(ema_5_8_distance.diff(), delta_x)

    df['ema_8_13_distance_slope_angle'] = get_angles(ema_8_13_distance.diff(), delta_x)
    df['ema_8_13_distance_slope_angle_diff'] = ema_8_13_distance.diff()
    df['ema_8_13_distance_slope_angle_diff_angle'] = get_angles(ema_8_13_distance.diff(), delta_x)

    df['ema_13_21_distance_slope_angle'] = get_angles(ema_13_21_distance.diff(), delta_x)
    df['ema_13_21_distance_slope_angle_diff'] = ema_13_21_distance.diff()
    df['ema_13_21_distance_slope_angle_diff_angle'] = get_angles(ema_13_21_distance.diff(), delta_x)


    # include MACD 6 3 5
    macd_6_13 = ta.trend.macd_diff(
        df["close"], window_slow=13, window_fast=16, window_sign=5, fillna=True
    )
    df['macd_6_13_slope_angle'] = get_angles(macd_6_13.diff(), delta_x)
    df['macd_6_13_slope_angle_diff'] = macd_6_13.diff()
    df['macd_6_13_slope_angle_diff_angle'] = get_angles(macd_6_13.diff(), delta_x)

    macd_6_13_ema = ta.trend.ema_indicator(macd_6_13, window=5)
    df['macd_6_13_ema_slope_angle'] = get_angles(macd_6_13_ema.diff(), delta_x)
    df['macd_6_13_ema_slope_angle_diff'] = macd_6_13_ema.diff()
    df['macd_6_13_ema_slope_angle_diff_angle'] = get_angles(macd_6_13_ema.diff(), delta_x)

    macd_6_13_close_ema_distance = macd_6_13 - macd_6_13_ema
    df['macd_6_13_close_ema_distance_slope_angle'] = get_angles(macd_6_13_close_ema_distance.diff(), delta_x)
    df['macd_6_13_close_ema_distance_slope_angle_diff'] = macd_6_13_close_ema_distance.diff()
    df['macd_6_13_close_ema_distance_slope_angle_diff_angle'] = get_angles(macd_6_13_close_ema_distance.diff(), delta_x)

    # include MACD 12 26 9
    macd_12_26 = ta.trend.macd_diff(
        df["close"], window_slow=26, window_fast=12, window_sign=9, fillna=True
    )
    df['macd_12_26_slope_angle'] = get_angles(macd_12_26.diff(), delta_x)
    df['macd_12_26_slope_angle_diff'] = macd_12_26.diff()
    df['macd_12_26_slope_angle_diff_angle'] = get_angles(macd_12_26.diff(), delta_x)


    macd_12_26_ema = ta.trend.ema_indicator(macd_12_26, window=9)
    df['macd_12_26_ema_slope_angle'] = get_angles(macd_12_26_ema.diff(), delta_x)
    df['macd_12_26_ema_slope_angle_diff'] = macd_12_26_ema.diff()
    df['macd_12_26_ema_slope_angle_diff_angle'] = get_angles(macd_12_26_ema.diff(), delta_x)

    macd_12_26_close_ema_distance = macd_12_26 - macd_12_26_ema
    df['macd_12_26_close_ema_distance_slope_angle'] = get_angles(macd_12_26_close_ema_distance.diff(), delta_x)
    df['macd_12_26_close_ema_distance_slope_angle_diff'] = macd_12_26_close_ema_distance.diff()
    df['macd_12_26_close_ema_distance_slope_angle_diff_angle'] = get_angles(macd_12_26_close_ema_distance.diff(), delta_x)

    # include stochastic 5 5 3
    stoch_5_5_k = ta.momentum.stoch(
        df["high"], df["low"], df["close"], window=5, smooth_window=5, fillna=True
    )
    df['stoch_5_5_k_slope_angle'] = get_angles(stoch_5_5_k.diff(), delta_x)
    df['stoch_5_5_k_slope_angle_diff'] = stoch_5_5_k.diff()
    df['stoch_5_5_k_slope_angle_diff_angle'] = get_angles(stoch_5_5_k.diff(), delta_x)

    stoch_5_5_d = ta.trend.sma_indicator(stoch_5_5_k, window=3)
    df['stoch_5_5_d_slope_angle'] = get_angles(stoch_5_5_d.diff(), delta_x)
    df['stoch_5_5_d_slope_angle_diff'] = stoch_5_5_d.diff()
    df['stoch_5_5_d_slope_angle_diff_angle'] = get_angles(stoch_5_5_d.diff(), delta_x)

    stoch_5_5_k_d_distance = stoch_5_5_k - stoch_5_5_d
    df['stoch_5_5_k_d_distance_slope_angle'] = get_angles(stoch_5_5_k_d_distance.diff(), delta_x)
    df['stoch_5_5_k_d_distance_slope_angle_diff'] = stoch_5_5_k_d_distance.diff()
    df['stoch_5_5_k_d_distance_slope_angle_diff_angle'] = get_angles(stoch_5_5_k_d_distance.diff(), delta_x)

    # include stochastic 10 10 6
    stoch_10_10_k = ta.momentum.stoch(
        df["high"], df["low"], df["close"], window=10, smooth_window=10, fillna=True
    )
    df['stoch_10_10_k_slope_angle'] = get_angles(stoch_10_10_k.diff(), delta_x)
    df['stoch_10_10_k_slope_angle_diff'] = stoch_10_10_k.diff()
    df['stoch_10_10_k_slope_angle_diff_angle'] = get_angles(stoch_10_10_k.diff(), delta_x)

    stoch_10_10_d = ta.trend.sma_indicator(stoch_10_10_k, window=6)
    df['stoch_10_10_d_slope_angle'] = get_angles(stoch_10_10_d.diff(), delta_x)
    df['stoch_10_10_d_slope_angle_diff'] = stoch_10_10_d.diff()
    df['stoch_10_10_d_slope_angle_diff_angle'] = get_angles(stoch_10_10_d.diff(), delta_x)

    stoch_10_10_k_d_distance = stoch_10_10_k - stoch_10_10_d
    df['stoch_10_10_k_d_distance_slope_angle'] = get_angles(stoch_10_10_k_d_distance.diff(), delta_x)
    df['stoch_10_10_k_d_distance_slope_angle_diff'] = stoch_10_10_k_d_distance.diff()
    df['stoch_10_10_k_d_distance_slope_angle_diff_angle'] = get_angles(stoch_10_10_k_d_distance.diff(), delta_x)


    new_df = add_lookback(df, 5)
    df = pd.concat([df, new_df], axis=1)


    # slope of the next candle
    df["next_close_slope_angle"] = get_angles(
        df["close"].shift(-1) - df["close"], delta_x
    )

    # filter prices that do not change
    close_changes = df["close"].shift(-1) - df["close"]
    high_changes = df["high"].shift(-1) - df["high"]
    low_changes = df["low"].shift(-1) - df["low"]

    df[(close_changes == 0) & (high_changes == 0) & (low_changes == 0)] = np.nan

    # use this for running simulation
    df["next_close"] = df["close"].shift(-1)

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
