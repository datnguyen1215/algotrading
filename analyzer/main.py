#!/usr/bin/python3
import lib.candles as candles
import lib.scaler as scaler
import lib.trainer as trainer
import dtale
from sklearn.preprocessing import MinMaxScaler
import uuid
import datetime
import joblib
import env
import os
from simulation.trade import Trade
import lib.features as features

def filter_candles(df):
    start_time = "00:00:00"
    end_time = "22:00:00"

    print("Filtering candles from " + start_time + " to " + end_time)
    df = df.between_time(start_time, end_time)
    print("Done filtering candles")

    # filter to weekdays
    print("Filtering candles to weekdays")
    df = df[df.index.dayofweek < 5]
    print("Done filtering candles to weekdays")

    return df


def start_training():


def simulate():
    print("Loading model and scaler...")
    model = joblib.load(env.MODEL_PATH)
    model_feature_scaler = joblib.load(env.SCALER_PATH)
    print("Done loading model and scaler")

    print("Getting candles...")
    df_5m = candles.get(env.SYMBOL, env.N_CANDLES)

    # should be used for calculating profit
    df_5m["next_close"] = df_5m["close"].shift(-1)

    df_5m = filter_candles(df_5m)
    print("Done getting candles")

    columns = features.NAMES + ["close", "next_close"]

    data_5m = df_5m[columns]

    data_5m = candles.remove_outliers(data_5m, columns)

    exclude_columns = ["close", "next_close"]

    [data_5m, data_5m_scaler] = scaler.scale(
        data_5m, model_feature_scaler, exclude_columns
    )

    data_5m.dropna(inplace=True)

    predictions = model.predict(data_5m[features.NAMES])
    data_5m["prediction"] = predictions

    # dtale.show(data_5m, subprocess=False, host="localhost").open_browser()

    print(data_5m.head(15))

    # iterate through the predictions and make trades
    balance = 100000
    trades = []
    for index, row in data_5m.iterrows():
        size = balance * 0.05
        if row["prediction"] > 0.7:
            t = Trade(
                env.SYMBOL,
                size,
                row["close"],
                index,
                row["next_close"],
                index + datetime.timedelta(minutes=5),
            )
            trades.append(t)
            balance += t.profit
            print(f"\rBalance: {balance}", end="")
        elif row["prediction"] < 0.3:
            t = Trade(
                env.SYMBOL,
                -size,
                row["close"],
                index,
                row["next_close"],
                index + datetime.timedelta(minutes=5),
            )
            trades.append(t)
            balance += t.profit
            print(f"\rBalance: {balance}", end="")

    print("\n")

    # calculate profits from all trades with self.profit using for loop
    profits = sum([t.profit for t in trades])
    print("Profits: " + str(profits))

    winning_trades = [t for t in trades if t.profit > 0]
    print("Winning trades: " + str(len(winning_trades)))

    losing_trades = [t for t in trades if t.profit < 0]
    print("Losing trades: " + str(len(losing_trades)))

    # calcculate win percentage
    win_percentage = len(winning_trades) / len(trades) * 100
    print(f"Win percentage: {win_percentage}%")


# get candles and plot
def main():
    print("Model path: " + env.MODEL_PATH)
    print("Scaler path: " + env.SCALER_PATH)
    print("Symbol: " + env.SYMBOL)
    print("N candles: " + str(env.N_CANDLES))

    if env.MODEL_PATH == "":
        train()
    else:
        simulate()


if __name__ == "__main__":
    main()
