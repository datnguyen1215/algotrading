#!/usr/bin/python3
import lib.features as features
import lib.candles as candles
import lib.scaler as scaler
import pandas as pd
import argparse
from lib.metatrader.expert import Expert
from lib.metatrader.server import start_server, accept_client
import lib.delta as delta
import math
import joblib
import matplotlib.pyplot as plt
import datetime
import pytz
import numpy as np


def get_models(symbol, model_directory):
    paths = {
        "5Min": f"{model_directory}/{symbol}_5Min",
        "15Min": f"{model_directory}/{symbol}_15Min",
        "30Min": f"{model_directory}/{symbol}_30Min",
        "1H": f"{model_directory}/{symbol}_1H",
        "2H": f"{model_directory}/{symbol}_2H",
        "4H": f"{model_directory}/{symbol}_4H",
        "6H": f"{model_directory}/{symbol}_6H",
        "1D": f"{model_directory}/{symbol}_1D",
    }

    models = {
        "5Min": joblib.load(f"{paths['5Min']}_m.joblib"),
        "15Min": joblib.load(f"{paths['15Min']}_m.joblib"),
        "30Min": joblib.load(f"{paths['30Min']}_m.joblib"),
        "1H": joblib.load(f"{paths['1H']}_m.joblib"),
        "2H": joblib.load(f"{paths['2H']}_m.joblib"),
        "4H": joblib.load(f"{paths['4H']}_m.joblib"),
        "6H": joblib.load(f"{paths['6H']}_m.joblib"),
        "1D": joblib.load(f"{paths['1D']}_m.joblib"),
    }

    return models


def wait_for_expert():
    server_socket = start_server()
    client_socket = accept_client(server_socket)

    expert = Expert(client_socket)
    return expert


def make_prediction(df, timeframe, feature_models):
    df = pd.DataFrame(df)

    # set 'time' as index datetime
    df["time"] = pd.to_datetime(df["time"])
    df = df.set_index("time")
    df = df.sort_index()

    df = candles.add_indicators(df)

    predictions = np.array([])
    for feature, model in feature_models.items():
        df_features = df[feature][-1:]
        pred = model.predict(df_features)
        predictions = np.append(predictions, pred)

    # get average of all predictions
    pred = np.average(predictions)

    # convert angles to price
    last_data = df.iloc[-1]
    last_close = last_data["close"]
    last_timestamp = (
        df.index[-1].tz_localize(pytz.timezone("Etc/GMT-2")).astimezone("Etc/GMT+5")
    )

    return [last_timestamp, last_close, pred]


def main(args):
    symbol = args.symbol
    n_candles = args.n_candles
    model_directory = args.model_directory

    expert = wait_for_expert()

    # go through all timeframes
    closes = []
    atrs = []
    averages = []
    timeframes = []
    timestamps = []

    all_models = get_models(symbol, model_directory)

    for timeframe, feature_models in all_models.items():
        df = expert.get_candles(symbol, timeframe, n_candles)

        # remove last candle since it's not complete
        df = df[:-1]

        [last_timestamp, last_close, pred] = make_prediction(
            df, timeframe, feature_models
        )

        df = pd.DataFrame(df)
        df = candles.add_indicators(df)

        # teriv calculations
        pred = pred / 4
        averages.append(pred)
        current_atr = df["atr"][-1:].values[0]
        atrs.append(current_atr)

        closes.append(last_close)
        timeframes.append(timeframe)
        timestamps.append(last_timestamp)
        print(f"Prediction for {timeframe}:")
        print(f"Time: {last_timestamp}, Last Close: {last_close}, Pred: {pred}")
        print("")

    # 4h - 1d
    D7 = averages[-3]
    B7 = averages[-1]
    I12 = (
        np.cos(np.arctan2((D7 - B7), (D7 + B7) / 2))
        * ((D7 - B7) ** 2 + ((D7 + B7) / 2) ** 2) ** 0.5
    )

    # shift -11.25+((abs(I12)))*(22.5)
    I9 = -11.25 + abs(I12) * 22.5

    # 5m bias (cos(atan2(I7-H7, (I7+H7)/2)+RADIANS(I9)))
    I7 = averages[0]
    H7 = averages[1]
    bias_5m = np.cos(np.arctan2((I7 - H7), (I7 + H7) / 2) + math.radians(I9))

    # 15m bias (cos(atan2(H7-F7, (H7+F7)/2)+RADIANS(I9)))
    H7 = averages[1]
    F7 = averages[3]
    bias_15m = np.cos(np.arctan2((H7 - F7), (H7 + F7) / 2) + math.radians(I9))

    # 30m bias (cos(atan2(G7-E7, (G7+E7)/2)+RADIANS(I9)))
    G7 = averages[2]
    E7 = averages[4]
    bias_30m = np.cos(np.arctan2((G7 - E7), (G7 + E7) / 2) + math.radians(I9))

    # 1h bias (cos(atan2(F7-D7, (F7+D7)/2)+RADIANS(I9)))
    F7 = averages[3]
    D7 = averages[5]
    bias_1h = np.cos(np.arctan2((F7 - D7), (F7 + D7) / 2) + math.radians(I9))

    # 2h bias (cos(atan2(E7-C7, (E7+C7)/2)+RADIANS(I9)))
    E7 = averages[4]
    C7 = averages[6]
    bias_2h = np.cos(np.arctan2((E7 - C7), (E7 + C7) / 2) + math.radians(I9))

    # 4h bias (cos(atan2(D7-B7, (D7+B7)/2)+RADIANS(I9)))
    D7 = averages[5]
    B7 = averages[7]
    bias_4h = np.cos(np.arctan2((D7 - B7), (D7 + B7) / 2) + math.radians(I9))

    # pip changes =D11*B11*((I7-H7)^2+((I7+H7)/2)^2)^0.5
    pip_5m = atrs[0] * bias_5m * ((I7 - H7) ** 2 + ((I7 + H7) / 2) ** 2) ** 0.5
    pip_15m = atrs[1] * bias_15m * ((H7 - F7) ** 2 + ((H7 + F7) / 2) ** 2) ** 0.5
    pip_30m = atrs[2] * bias_30m * ((G7 - E7) ** 2 + ((G7 + E7) / 2) ** 2) ** 0.5
    pip_1h = atrs[3] * bias_1h * ((F7 - D7) ** 2 + ((F7 + D7) / 2) ** 2) ** 0.5
    pip_2h = atrs[4] * bias_2h * ((E7 - C7) ** 2 + ((E7 + C7) / 2) ** 2) ** 0.5
    pip_4h = atrs[5] * bias_4h * ((D7 - B7) ** 2 + ((D7 + B7) / 2) ** 2) ** 0.5

    # minutes on x-axis
    x = [timestamps[0]] + [
        timestamps[0] + datetime.timedelta(minutes=delta.MINUTES[timeframe])
        for timeframe in timeframes
    ]
    x = [x.strftime("%H:%M") for x in x][:-2]
    preds = [pip_5m, pip_15m, pip_30m, pip_1h, pip_2h, pip_4h]
    y = [0] + preds
    print(x)
    print(y)
    plt.plot(x, y)
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.title(f"{symbol} Changes over Time")
    plt.axhline(y=0, color="r", linestyle="-")
    plt.show()


if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", help="Symbol to train", default="EURUSD")
    parser.add_argument("--n_candles", help="Number of candles to train", default=500)
    parser.add_argument(
        "--model_directory", help="Directory to save the model", default="models"
    )
    args = parser.parse_args()
    main(args)
