import numpy as np
import ta
import pandas as pd


def add(df: pd.DataFrame, n_lookback=9):
    """
    Add indicators to the dataframe

    :param df: dataframe
    :param n_lookback: number of lookback periods

    :return: dataframe
    """

    # ichimoku cloud
    ichimoku_df = ichimoku_angles(df, n_lookback=n_lookback)

    # bollinger bands

    return df


def ichimoku_angles(df: pd.DataFrame, n_lookback=9):
    """
    Add ichimoku cloud to the dataframe

    :param df: dataframe
    :param n_lookback: number of lookback periods

    :return: dataframe
    """
    result_df = pd.DataFrame()

    # ichimoku cloud
    ichimoku_a = ta.trend.ichimoku_a(df["high"], df["low"])
    ichimoku_b = ta.trend.ichimoku_b(df["high"], df["low"])
    ichimoku_base = ta.trend.ichimoku_base_line(df["high"], df["low"])
    ichimoku_conversion = ta.trend.ichimoku_conversion_line(df["high"], df["low"])

    # add distance
    ichimoku_a_b_distances = ichimoku_a - ichimoku_b
    ichimoku_a_base_distances = ichimoku_a - ichimoku_base
    ichimoku_a_conversion_distances = ichimoku_a - ichimoku_conversion
    ichimoku_a_close_distances = ichimoku_a - df['close']
    ichimoku_b_base_distances = ichimoku_b - ichimoku_base
    ichimoku_b_conversion_distances = ichimoku_b - ichimoku_conversion
    ichimoku_b_close_distances = ichimoku_b - df['close']
    ichimoku_base_conversion_distances = ichimoku_base - ichimoku_conversion
    ichimoku_base_close_distances = ichimoku_base - df['close']
    ichimoku_conversion_close_distances = ichimoku_conversion - df['close']

    # add angles
    ichimoku_a_b_distance_angles = _get_angles(ichimoku_a_b_distances)
    ichimoku_a_base_distance_angles = _get_angles(ichimoku_a_base_distances)
    ichimoku_a_conversion_distance_angles = _get_angles(ichimoku_a_conversion_distances)
    ichimoku_a_close_distance_angles = _get_angles(ichimoku_a_close_distances)
    ichimoku_b_base_distance_angles = _get_angles(ichimoku_b_base_distances)
    ichimoku_b_conversion_distance_angles = _get_angles(ichimoku_b_conversion_distances)
    ichimoku_b_close_distance_angles = _get_angles(ichimoku_b_close_distances)
    ichimoku_base_conversion_distance_angles = _get_angles(ichimoku_base_conversion_distances)
    ichimoku_base_close_distance_angles = _get_angles(ichimoku_base_close_distances)
    ichimoku_conversion_close_distance_angles = _get_angles(ichimoku_conversion_close_distances)

    # add lookback
    for i in range(1, n_lookback + 1):
        result_df['ichimoku_a_b_distance_angle_' + str(i)] = ichimoku_a_b_distance_angles.shift(i)
        result_df['ichimoku_a_base_distance_angle_' + str(i)] = ichimoku_a_base_distance_angles.shift(i)
        result_df['ichimoku_a_conversion_distance_angle_' + str(i)] = ichimoku_a_conversion_distance_angles.shift(i)
        result_df['ichimoku_a_close_distance_angle_' + str(i)] = ichimoku_a_close_distance_angles.shift(i)
        result_df['ichimoku_b_base_distance_angle_' + str(i)] = ichimoku_b_base_distance_angles.shift(i)
        result_df['ichimoku_b_conversion_distance_angle_' + str(i)] = ichimoku_b_conversion_distance_angles.shift(i)
        result_df['ichimoku_b_close_distance_angle_' + str(i)] = ichimoku_b_close_distance_angles.shift(i)
        result_df['ichimoku_base_conversion_distance_angle_' + str(i)] = ichimoku_base_conversion_distance_angles.shift(i)
        result_df['ichimoku_base_close_distance_angle_' + str(i)] = ichimoku_base_close_distance_angles.shift(i)
        result_df['ichimoku_conversion_close_distance_angle_' + str(i)] = ichimoku_conversion_close_distance_angles.shift(i)

    return result_df

def _add_lookback(series: pd.Series, column_name, n_lookback=9):
    """
    Add lookback columns to a series

    :param series: series
    :param column_name: column name
    :param n_lookback: number of lookback periods

    :return: series
    """

    for i in range(1, n_lookback + 1):
        series[f"{column_name}_{i}"] = series[column_name].shift(i)

    return series

def _get_angles(y_diff_series: pd.Series, delta_x=1):
    """
    Get angles from a series of y differences

    :param series: series
    :param delta_x: delta x

    :return: series
    """

    slopes = y_diff_series / delta_x
    angles = np.arctan(slopes)
    return np.degrees(angles)