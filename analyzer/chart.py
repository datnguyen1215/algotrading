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


def main(args):
    symbol = args.symbol
    n_candles = args.n_candles
    model_directory = args.model_directory

    server_socket = start_server()
    client_socket = accept_client(server_socket)

    expert = Expert(client_socket)

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
        "5Min": joblib.load(f"{paths['5Min']}_m"),
        "15Min": joblib.load(f"{paths['15Min']}_m"),
        "30Min": joblib.load(f"{paths['30Min']}_m"),
        "1H": joblib.load(f"{paths['1H']}_m"),
        "2H": joblib.load(f"{paths['2H']}_m"),
        "4H": joblib.load(f"{paths['4H']}_m"),
        "6H": joblib.load(f"{paths['6H']}_m"),
    }

    feature_scalers = {
        "5Min": joblib.load(f"{paths['5Min']}_fs"),
        "15Min": joblib.load(f"{paths['15Min']}_fs"),
        "30Min": joblib.load(f"{paths['30Min']}_fs"),
        "1H": joblib.load(f"{paths['1H']}_fs"),
        "2H": joblib.load(f"{paths['2H']}_fs"),
        "4H": joblib.load(f"{paths['4H']}_fs"),
        "6H": joblib.load(f"{paths['6H']}_fs"),
    }

    target_scalers = {
        "5Min": {
            "positive": joblib.load(f"{paths['5Min']}_pts"),
            "negative": joblib.load(f"{paths['5Min']}_nts"),
        },
        "15Min": {
            "positive": joblib.load(f"{paths['15Min']}_pts"),
            "negative": joblib.load(f"{paths['15Min']}_nts"),
        },
        "30Min": {
            "positive": joblib.load(f"{paths['30Min']}_pts"),
            "negative": joblib.load(f"{paths['30Min']}_nts"),
        },
        "1H": {
            "positive": joblib.load(f"{paths['1H']}_pts"),
            "negative": joblib.load(f"{paths['1H']}_nts"),
        },
        "2H": {
            "positive": joblib.load(f"{paths['2H']}_pts"),
            "negative": joblib.load(f"{paths['2H']}_nts"),
        },
        "4H": {
            "positive": joblib.load(f"{paths['4H']}_pts"),
            "negative": joblib.load(f"{paths['4H']}_nts"),
        },
        "6H": {
            "positive": joblib.load(f"{paths['6H']}_pts"),
            "negative": joblib.load(f"{paths['6H']}_nts"),
        },
    }

    def make_prediction(symbol, timeframe):
        data = expert.get_candles(symbol, timeframe, n_candles)
        df = pd.DataFrame(data)
        print(df.tail())

        # set 'time' as index datetime
        df["time"] = pd.to_datetime(df["time"])
        df = df.set_index("time")

        df = candles.add_indicators(df)
        df.dropna(inplace=True)

        [df_features, df_scaler] = scaler.scale(
            df[features.NAMES], feature_scalers[timeframe]
        )

        # note: last candle isn't completed, so we'll remove it from the dataframe
        predictions = models[timeframe].predict(df_features[-2:-1])
        angles = scale_predictions(predictions, timeframe)

        # each prediction is an angle of the movement, so we need to convert it to a price
        # we'll use the last close price as a reference

        [pred_high_angle, pred_close_angle, pred_low_angle] = angles[0]

        # convert angles to price
        last_close = df["close"].iloc[0]
        last_high = df["high"].iloc[0]
        last_low = df["low"].iloc[0]

        # get radians of angle
        pred_high_r = pred_high_angle * (math.pi / 180)
        pred_close_r = pred_close_angle * (math.pi / 180)
        pred_low_r = pred_low_angle * (math.pi / 180)

        # convert radians into tangent of the angle
        pred_high_t = math.tan(pred_high_r)
        pred_close_t = math.tan(pred_close_r)
        pred_low_t = math.tan(pred_low_r)

        # Multiple slope by delta_x
        pred_high_slope = pred_high_t * delta.MINUTES[timeframe]
        pred_close_slope = pred_close_t * delta.MINUTES[timeframe]
        pred_low_slope = pred_low_t * delta.MINUTES[timeframe]

        pred_high = last_high + pred_high_slope
        pred_close = last_close + pred_close_slope
        pred_low = last_low + pred_low_slope

        return [pred_high, pred_close, pred_low]

    def scale_predictions(original_preds, timeframe):
        # scale the predictions back to original form
        # anything that's negative, use the negative scaler
        # anything that's positive, use the positive scaler

        predictions = original_preds.copy()

        # make a copy for < 0.5 and >= 0.5
        negative_predictions = predictions.copy()
        positive_predictions = predictions.copy()

        # set anything >= 0.5 to 0
        negative_predictions[negative_predictions >= 0.5] = 0

        # set anything < 0.5 to 0
        positive_predictions[positive_predictions < 0.5] = 0

        # scale the negative predictions
        negative_predictions = target_scalers[timeframe]["negative"].inverse_transform(
            negative_predictions
        )

        # scale the positive predictions
        positive_predictions = target_scalers[timeframe]["positive"].inverse_transform(
            positive_predictions
        )

        # if original_preds value is < 0, use negative predictions
        # if original_preds value is >= 0, use positive predictions
        for i in range(len(predictions)):
            for j in range(len(predictions[i])):
                if predictions[i][j] < 0.5:
                    predictions[i][j] = negative_predictions[i][j]
                else:
                    predictions[i][j] = positive_predictions[i][j]

        return predictions

    # go through all timeframes
    for timeframe in models:
        [pred_high, pred_close, pred_low] = make_prediction(symbol, timeframe)
        print(f"Prediction for {timeframe}:")
        print(f"High: {pred_high}")
        print(f"Close: {pred_close}")
        print(f"Low: {pred_low}")
        print("")


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
