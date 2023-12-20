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
    }

    models = {
        "5Min": joblib.load(f"{paths['5Min']}_m.joblib"),
        "15Min": joblib.load(f"{paths['15Min']}_m.joblib"),
        "30Min": joblib.load(f"{paths['30Min']}_m.joblib"),
        "1H": joblib.load(f"{paths['1H']}_m.joblib"),
        "2H": joblib.load(f"{paths['2H']}_m.joblib"),
        "4H": joblib.load(f"{paths['4H']}_m.joblib"),
        "6H": joblib.load(f"{paths['6H']}_m.joblib"),
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

    # remove last candle since it's not complete
    df = df[:-1]

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

    # get radians of angle
    pred_angle = pred
    pred_close_r = pred_angle * (math.pi / 180)
    pred_close_t = math.tan(pred_close_r)
    pred_close_slope = pred_close_t * delta.MINUTES[timeframe]
    pred_close = last_close + pred_close_slope

    return [last_timestamp, last_close, pred_close]


def main(args):
    symbol = args.symbol
    n_candles = args.n_candles
    model_directory = args.model_directory

    expert = wait_for_expert()

    # go through all timeframes
    closes = []
    preds = []
    timeframes = []
    timestamps = []

    all_models = get_models(symbol, model_directory)

    for timeframe, feature_models in all_models.items():
        df = expert.get_candles(symbol, timeframe, n_candles)
        [last_timestamp, last_close, pred_close] = make_prediction(
            df, timeframe, feature_models
        )
        preds.append(pred_close)
        closes.append(last_close)
        timeframes.append(timeframe)
        timestamps.append(last_timestamp)
        print(f"Prediction for {timeframe}:")
        print(
            f"Time: {last_timestamp}, Last Close: {last_close}, Pred: {pred_close}, Change: {pred_close - last_close}"
        )
        print("")

    # minutes on x-axis
    x = [timestamps[0]] + [
        timestamps[0] + datetime.timedelta(minutes=delta.MINUTES[timeframe])
        for timeframe in timeframes
    ]
    x = [x.strftime("%H:%M") for x in x]
    preds = [p - closes[0] for p in preds]
    y = [0] + preds
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
