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


def remove_outliers(df, columns):
    # remove target outliers
    Q1 = df[columns].quantile(0.25)
    Q3 = df[columns].quantile(0.75)
    IQR = Q3 - Q1
    tmp = df[~((df[columns] < (Q1 - 1.5 * IQR)) | (df[columns] > (Q3 + 1.5 * IQR)))]
    df[columns] = tmp[columns]
    return df


def train(symbol, original_df, timeframe, feature_columns, target_columns):
    print(f"Training {symbol} {timeframe}...")

    # make a copy and get only the features
    df = original_df.copy()

    if timeframe != "5Min":
        df = candles.resample_df(df, timeframe)

    delta_map = {
        "5Min": 5,
        "15Min": 15,
        "30Min": 30,
        "1H": 60,
        "2H": 120,
        "4H": 240,
        "6H": 360,
    }

    df = candles.add_indicators(df, delta_map[timeframe])

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

    # scale the features only
    [df_features, data_5m_scaler] = scaler.scale(df[feature_columns])

    [df_targets, neg_target_scaler, pos_target_scaler] = scaler.scale_angle(
        df[target_columns]
    )

    # need to set index back to df. Scaler removes the index for some reasons.
    df_features.set_index(df.index, inplace=True)
    df[feature_columns] = df_features

    # need to set index back to df. Scaler removes the index for some reasons.
    df_targets.set_index(df.index, inplace=True)
    df[target_columns] = df_targets

    # need to drop NaNs after scaling, otherwise, it'll contain NaNs for some reasons.
    df.dropna(inplace=True)

    # split data into 20% test and 80% train
    test_df = df.tail(int(len(df) * 0.2))
    df = df.head(int(len(df) * 0.8))

    model = trainer.train(df[feature_columns + target_columns], target_columns)

    predictions = model.predict(test_df[feature_columns])
    trades = []
    balance = 100000

    # simulate trades
    for i in range(1, len(test_df)):
        [pred_high, pred_close, pred_low] = predictions[i]
        next_close = test_df.iloc[i]["next_close"]
        close = test_df.iloc[i]["close"]
        risk = balance * 0.01
        size = risk / close

        # long
        if pred_high > 0.5 and pred_close > 0.5:
            trades.append(Trade(symbol, size, close, None, next_close, None))
            balance += trades[-1].profit

        # short
        if pred_close < 0.5 and pred_low < 0.5:
            trades.append(Trade(symbol, -size, close, None, next_close, None))
            balance += trades[-1].profit

        trades = [t for t in trades]
        wins = [t for t in trades if t.profit > 0]
        loses = [t for t in trades if t.profit < 0]

        print(
            f"\rBalance: {balance}, Trades: {trades}, Win/Lose: {wins}/{loses}, Win Rate: {(len(wins) / len(trades)):0.2f}%",
            end="",
        )

    print("")

    # check if models directory exists
    if not os.path.exists("models"):
        os.makedirs("models")

    joblib.dump(model, f"models/{symbol}_{timeframe}_m")
    joblib.dump(data_5m_scaler, f"models/{symbol}_{timeframe}_fs")
    joblib.dump(neg_target_scaler, f"models/{symbol}_{timeframe}_nts")
    joblib.dump(pos_target_scaler, f"models/{symbol}_{timeframe}_pts")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", help="Symbol to train", default="EURUSD")
    parser.add_argument("--n_candles", help="Number of candles to train", default=15000)
    args = parser.parse_args()

    print(f"args.symbol: {args.symbol}, args.n_candles: {args.n_candles}")

    df = candles.get(args.symbol, args.n_candles)

    target_columns = [
        "next_high_slope_angle",
        "next_close_slope_angle",
        "next_low_slope_angle",
    ]

    train(args.symbol, df, "5Min", features.NAMES, target_columns)
    train(args.symbol, df, "15Min", features.NAMES, target_columns)
    train(args.symbol, df, "30Min", features.NAMES, target_columns)
    train(args.symbol, df, "1H", features.NAMES, target_columns)
    train(args.symbol, df, "2H", features.NAMES, target_columns)
    train(args.symbol, df, "4H", features.NAMES, target_columns)
    train(args.symbol, df, "6H", features.NAMES, target_columns)


if __name__ == "__main__":
    main()
