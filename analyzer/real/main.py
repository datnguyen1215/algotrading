#!/usr/bin/python3

from metatrader.server import start_server, accept_client
from metatrader.expert import Expert
import candles
import pandas as pd
import time
import scaler
import joblib
import env
import schedule
import datetime


COLUMNS_TO_KEEP = [
    "avg_ema_3_slope_angle",
    # "avg_ema_3_slope_angle_2",
    # "avg_ema_3_slope_angle_3",
    "avg_ema_5_slope_angle",
    # "avg_ema_5_slope_angle_2",
    # "avg_ema_5_slope_angle_3",
    "rsi_7_slope_angle",
    # "rsi_7_slope_angle_2",
    # "rsi_7_slope_angle_3",
    "rsi_7_sma_slope_angle",
    # "rsi_7_sma_slope_angle_2",
    # "rsi_7_sma_slope_angle_3",
    "rsi_14_slope_angle",
    # "rsi_14_slope_angle_2",
    # "rsi_14_slope_angle_3",
    "rsi_14_sma_slope_angle",
    # "rsi_14_sma_slope_angle_2",
    # "rsi_14_sma_slope_angle_3",
    "macd_6_13_slope_angle",
    # "macd_6_13_slope_angle_2",
    # "macd_6_13_slope_angle_3",
    "macd_6_13_ema_slope_angle",
    # "macd_6_13_ema_slope_angle_2",
    # "macd_6_13_ema_slope_angle_3",
    "macd_12_26_slope_angle",
    # "macd_12_26_slope_angle_2",
    # "macd_12_26_slope_angle_3",
    "macd_12_26_ema_slope_angle",
    # "macd_12_26_ema_slope_angle_2",
    # "macd_12_26_ema_slope_angle_3",
    "stoch_5_5_k_slope_angle",
    # "stoch_5_5_k_slope_angle_2",
    # "stoch_5_5_k_slope_angle_3",
    "stoch_5_5_d_slope_angle",
    # "stoch_5_5_d_slope_angle_2",
    # "stoch_5_5_d_slope_angle_3",
    "stoch_10_10_k_slope_angle",
    # "stoch_10_10_k_slope_angle_2",
    # "stoch_10_10_k_slope_angle_3",
    "stoch_10_10_d_slope_angle",
    # "stoch_10_10_d_slope_angle_2",
    # "stoch_10_10_d_slope_angle_3",
    "di_plus_slope_angle",
    # "di_plus_slope_angle_2",
    # "di_plus_slope_angle_3",
    "di_minus_slope_angle",
    # "di_minus_slope_angle_2",
    # "di_minus_slope_angle_3",
]

if __name__ == "__main__":
    server_socket = start_server()
    client_socket = accept_client(server_socket)

    expert = Expert(client_socket)

    model = joblib.load(env.MODEL_PATH)
    model_feature_scaler = joblib.load(env.SCALER_PATH)

    def make_prediction():
        data = expert.get_candles("CADJPY", "M5", 500)
        df = pd.DataFrame(data)

        # set 'time' as index datetime
        df["time"] = pd.to_datetime(df["time"])
        df = df.set_index("time")

        last_timestamp = df.index[-1]
        current_time = pd.Timestamp.now()

        # seconds_difference = (current_time - last_timestamp).total_seconds()
        # if seconds_difference < 4*60 + 55:
        #     df = df[:-1]

        df = candles.add_indicators(df)
        df = df[COLUMNS_TO_KEEP]
        print(df.tail(1))
        df.dropna(inplace=True)

        [df, data_5m_scaler] = scaler.scale(df, model_feature_scaler)

        # get the last data
        last_data = df[-3:]
        print(last_data)
        predictions = model.predict(last_data)

        if predictions[-2] > 0.5:
            print(f"{last_data.index[-2]} - BUY - {predictions[-2]}")
        else:
            print(f"{last_data.index[-2]} - SELL - {predictions[-2]}")

        if predictions[-1] > 0.5:
            print(f"{last_data.index[-1]} - BUY - {predictions[-1]}")
        else:
            print(f"{last_data.index[-1]} - SELL - {predictions[-1]}")

    make_prediction()
    schedule.every(15).seconds.do(make_prediction)

    while True:
        schedule.run_pending()
        time.sleep(1)
