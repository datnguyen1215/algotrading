#!/usr/bin/python3
import candles
import scaler
import trainer
import dtale
from sklearn.preprocessing import MinMaxScaler
import uuid
import datetime
import joblib


# get candles and plot
def main():
    # generate new uuid
    program_id = uuid.uuid4()

    print("Program ID: " + str(program_id))

    start_time = "00:00:00"
    end_time = "22:00:00"

    print("Fetching candles...")
    df_5m = candles.get()
    print("Got candles")

    # filter specific time of the day
    print("Filtering candles from " + start_time + " to " + end_time)
    df_5m = df_5m.between_time(start_time, end_time)
    print("Done filtering candles")

    # filter to weekdays
    print("Filtering candles to weekdays")
    df_5m = df_5m[df_5m.index.dayofweek < 5]
    print("Done filtering candles to weekdays")

    # d = dtale.show(df_5m, subprocess=False, host="localhost")
    # d.open_browser()

    columns_to_keep = [
        "avg_ema_3_slope_angle",
        "avg_ema_5_slope_angle",
        # "avg_ema_8_slope_angle",
        # "avg_ema_13_slope_angle",
        # "avg_ema_21_slope_angle",
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
        "target"
    ]

    data_5m = df_5m[columns_to_keep]
    data_5m = candles.remove_outliers(data_5m, columns_to_keep)

    target = data_5m["target"]
    data_5m = data_5m.drop(["target"], axis=1)
    [data_5m, data_5m_scaler] = scaler.scale(data_5m)
    data_5m["target"] = scaler.scale_target(target)
    print(data_5m[['target']].head(15))

    data_5m.dropna(inplace=True)


    # d = dtale.show(data_5m, subprocess=False, host="localhost")
    # d.open_browser()

    model = trainer.train(data_5m)
    
    # Get the current date and time
    now = datetime.datetime.now()

    # Format the current date and time as a string in the format 'YYYYMMDD_HHMMSS'
    # For example: '20230401_153045'
    formatted_now = now.strftime('%Y%m%d_%H%M%S')

    model_name = f"models/{formatted_now}_{str(program_id)}_model.keras"
    model.save(model_name)

    # save the scaler
    scaler_name = f"models/{formatted_now}_{str(program_id)}_scaler.pkl"
    joblib.dump(data_5m_scaler, scaler_name)

if __name__ == "__main__":
    main()
