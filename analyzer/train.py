#!/usr/bin/python3
from lib import features
from lib import candles
from lib import trainer
from lib import scaler
import dtale
import joblib
import os
import argparse
from simulation.trade import Trade
import numpy as np
import pandas as pd
from lib import targets
import lib.delta as DELTA


def print_inline(text):
    # get the previous text size
    size = len(text)

    # print the text
    print(text, end="")
    # print spaces to clear the previous text
    print(" " * (100 - size), end="")
    # move the cursor back to the beginning of the line
    print("\r", end="")
    # flush the buffer
    print("", end="", flush=True)


def filter_candles(df):
    start_time = "10:00:00"
    end_time = "23:00:00"

    print("Filtering candles from " + start_time + " to " + end_time)
    df = df.between_time(start_time, end_time)
    print("Done filtering candles")

    # filter to weekdays
    print("Filtering candles to weekdays")
    df = df[df.index.dayofweek < 5]
    print("Done filtering candles to weekdays")

    return df


def remove_outliers(df, columns):
    # remove target outliers
    Q1 = df[columns].quantile(0.25)
    Q3 = df[columns].quantile(0.75)
    IQR = Q3 - Q1
    tmp = df[~((df[columns] < (Q1 - 1.5 * IQR)) | (df[columns] > (Q3 + 1.5 * IQR)))]
    df[columns] = tmp[columns]
    return df


def remove_outliers_using_bins(df, column, n_bins):
    bins = pd.cut(df[column], n_bins, labels=False)

    # remove those that are more than count averae
    df["bins"] = bins
    df["bins_count"] = df.groupby("bins")["bins"].transform("count")
    df = df[df["bins_count"] < df["bins_count"].mean()]
    df.drop(["bins_count"], axis=1, inplace=True)
    df.drop(["bins"], axis=1, inplace=True)

    return df


def simulate_test(df, predictions):
    results = []
    trades = []
    balance = 100000

    # simulate trades
    for i in range(0, len(df)):
        pred_close = predictions[i]
        next_close = df.iloc[i]["next_close"]
        close = df.iloc[i]["close"]
        risk = balance * 0.01
        size = risk / close

        # long
        if pred_close > 0.5:
            trades.append(Trade("", size, close, None, next_close, None))
            balance += trades[-1].profit
            if trades[-1].profit > 0:
                results.append(1)
            else:
                results.append(-1)

        # short
        if pred_close < 0.5:
            trades.append(Trade("", -size, close, None, next_close, None))
            balance += trades[-1].profit

            if trades[-1].profit > 0:
                results.append(1)
            else:
                results.append(-1)

        if pred_close == 0.5:
            results.append(0)

        wins = [t for t in trades if t.profit > 0]
        loses = [t for t in trades if t.profit < 0]
        buys = [t for t in trades if t.size > 0]
        sells = [t for t in trades if t.size < 0]

        print_inline(
            f"\rBalance: {balance}, Trades: {len(trades)}, Win/Lose: {len(wins)}/{len(loses)}, Win Rate: {(len(wins) / len(trades) * 100):0.2f}%, Buy/Sell: {len(buys)}/{len(sells)}"
        )

    print("")

    print(f"predictions length: {len(predictions)}, results length: {len(results)}")


def train_models(df, feature_columns, target_columns):
    # train multiple models, each for a single feature
    models = {}
    for feature in feature_columns:
        print(f"Training model for {feature}...")
        model = trainer.train(df[[feature] + target_columns], target_columns)
        models[feature] = model

    return models


def train(symbol, original_df, timeframe, feature_columns, target_columns):
    print(f"Training {symbol} {timeframe}...")

    # make a copy and get only the features
    df = original_df.copy()

    if timeframe != "5Min":
        df = candles.resample_df(df, timeframe)

    df = candles.add_indicators(df, DELTA.MINUTES[timeframe])

    # should drop NaNs after adding indicators, some of them has NaNs
    df.dropna(inplace=True)

    # remove target outliers first so we can scale the target properly
    df = remove_outliers(df, target_columns)

    # remove_outliers sometimes would have NaNs, so we need to drop them
    df.dropna(inplace=True)

    # remove feature outliers so we can scale the features properly
    df = remove_outliers(df, feature_columns)

    # remove_outliers sometimes would have NaNs, so we need to drop them
    df.dropna(inplace=True)

    models = train_models(df, feature_columns, target_columns)

    # check if models directory exists
    if not os.path.exists("models"):
        os.makedirs("models")

    # save all models into a single file
    joblib.dump(models, f"models/{symbol}_{timeframe}_m.joblib")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", help="Symbol to train", default="EURUSD")
    parser.add_argument("--n_candles", help="Number of candles to train", default=15000)
    args = parser.parse_args()

    print(f"args.symbol: {args.symbol}, args.n_candles: {args.n_candles}")

    df = candles.get(args.symbol, args.n_candles)

    train(args.symbol, df, "5Min", features.NAMES, targets.NAMES)
    train(args.symbol, df, "15Min", features.NAMES, targets.NAMES)
    train(args.symbol, df, "30Min", features.NAMES, targets.NAMES)
    train(args.symbol, df, "1H", features.NAMES, targets.NAMES)
    train(args.symbol, df, "2H", features.NAMES, targets.NAMES)
    train(args.symbol, df, "4H", features.NAMES, targets.NAMES)
    train(args.symbol, df, "6H", features.NAMES, targets.NAMES)


if __name__ == "__main__":
    main()
