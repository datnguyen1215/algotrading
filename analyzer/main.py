#!/usr/bin/python3
import candles
import scaler
import trainer
import dtale
from sklearn.preprocessing import MinMaxScaler
import uuid
import datetime
import joblib
import env
import os
from simulation.trade import Trade
from tensorflow.keras.models import load_model

COLUMNS_TO_KEEP = [
    "avg_ema_3_slope_angle",
    "avg_ema_5_slope_angle",
    "rsi_7_slope_angle",
    "rsi_7_sma_slope_angle",
    "rsi_14_slope_angle",
    "rsi_14_sma_slope_angle",
    "macd_6_13_slope_angle",
    "macd_6_13_ema_slope_angle",
    "macd_12_26_slope_angle",
    "macd_12_26_ema_slope_angle",
    "stoch_5_5_k_slope_angle",
    "stoch_5_5_d_slope_angle",
    "stoch_10_10_k_slope_angle",
    "stoch_10_10_d_slope_angle",
    "di_plus_slope_angle",
    "di_minus_slope_angle",
]


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


def train():
    # generate new uuid
    program_id = uuid.uuid4()

    print("Program ID: " + str(program_id))

    df_5m = candles.get(env.SYMBOL, env.N_CANDLES)
    df_5m = filter_candles(df_5m)

    # d = dtale.show(df_5m, subprocess=False, host="localhost")
    # d.open_browser()

    columns = COLUMNS_TO_KEEP + ["prev_close_slope_angle"]

    data_5m = df_5m[columns]
    print(data_5m.head(15))

    # remove target outliers
    Q1 = data_5m["prev_close_slope_angle"].quantile(0.25)
    Q3 = data_5m["prev_close_slope_angle"].quantile(0.75)
    IQR = Q3 - Q1
    data_5m = data_5m[
        ~(
            (data_5m["prev_close_slope_angle"] < (Q1 - 1.5 * IQR))
            | (data_5m["prev_close_slope_angle"] > (Q3 + 1.5 * IQR))
        )
    ]

    data_5m.dropna(inplace=True)

    data_5m = candles.remove_outliers(data_5m, columns)

    target = data_5m["prev_close_slope_angle"]
    data_5m.drop("prev_close_slope_angle", axis=1, inplace=True)

    [data_5m, data_5m_scaler] = scaler.scale(data_5m)

    data_5m["target"] = scaler.scale_target(target)

    # need to drop NaNs after scaling, otherwise, it'll contain NaNs for some reasons.
    data_5m.dropna(inplace=True)

    # need to +4 to map it from 0 to 8. Otherwise, we'll have problems with
    # classifier.
    data_5m["target"] = data_5m["target"].round().astype(int) + 4

    print(data_5m.head(15))

    # d = dtale.show(data_5m, subprocess=False, host="localhost")
    # d.open_browser()

    model = trainer.train(data_5m)

    # Get the current date and time
    now = datetime.datetime.now()

    # Format the current date and time as a string in the format 'YYYYMMDD_HHMMSS'
    # For example: '20230401_153045'
    formatted_now = now.strftime("%Y%m%d_%H%M%S")

    # check if models directory exists
    if not os.path.exists("models"):
        os.makedirs("models")

    model_name = f"models/{formatted_now}_{str(program_id)}_model.keras"
    model.save(model_name)

    # save the scaler
    scaler_name = f"models/{formatted_now}_{str(program_id)}_scaler.pkl"
    joblib.dump(data_5m_scaler, scaler_name)


def simulate():
    print("Loading model and scaler...")
    model = load_model(env.MODEL_PATH)
    model_feature_scaler = joblib.load(env.SCALER_PATH)
    print("Done loading model and scaler")

    print("Getting candles...")
    df_5m = candles.get(env.SYMBOL, env.N_CANDLES)
    print(df_5m.head(15))

    # should be used for calculating profit
    df_5m["next_close"] = df_5m["close"].shift(-1)

    df_5m = filter_candles(df_5m)
    print("Done getting candles")

    columns = COLUMNS_TO_KEEP + ["close", "next_close"]

    data_5m = df_5m[columns]
    print(data_5m.head(15))

    data_5m = candles.remove_outliers(data_5m, columns)

    exclude_columns = ["close", "next_close"]

    [data_5m, data_5m_scaler] = scaler.scale(
        data_5m, model_feature_scaler, exclude_columns
    )

    data_5m.dropna(inplace=True)

    predictions = model.predict(data_5m[COLUMNS_TO_KEEP])

    # get the exact prediction based on multi-class classification
    predictions = predictions.argmax(axis=1)

    data_5m["prediction"] = predictions.round().astype(int)
    
    # iterate through the predictions and make trades
    trades = []
    for index, row in data_5m.iterrows():
        if row["prediction"] > 4:
            t = Trade(env.SYMBOL, 1, row["close"], index, row["next_close"], index + datetime.timedelta(minutes=5))
            trades.append(t)
            print(f"Buy at {row['close']} at {index}: {t.profit}")
        elif row["prediction"] < 4:
            t = Trade(env.SYMBOL, -1, row["close"], index, row["next_close"], index + datetime.timedelta(minutes=5))
            trades.append(t)
            print(f"Sell at {row['close']} at {index}: {t.profit}")
            
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
