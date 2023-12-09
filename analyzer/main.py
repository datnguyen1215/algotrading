#!/usr/bin/python3
import candles
import scaler
import trainer
import dtale
from sklearn.preprocessing import StandardScaler, MinMaxScaler


# get candles and plot
def main():
    start_time = "00:00:00"
    end_time = "17:00:00"

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
        # "rsi_7_sma_slope_angle",
        # "rsi_14_slope_angle",
        # "rsi_14_sma_slope_angle",
        "macd_6_13_slope_angle",
        # "macd_6_13_ema_slope_angle",
        # "macd_12_26_slope_angle",
        # "macd_12_26_ema_slope_angle",
        "stoch_5_5_k_slope_angle",
        "stoch_5_5_d_slope_angle",
        # "stoch_10_10_k_slope_angle",
        # "stoch_10_10_d_slope_angle",
        "di_plus_slope_angle",
        "di_minus_slope_angle",
        # "avg_ema_3_5_diff",
        # "avg_ema_3_8_diff",
        # "avg_ema_3_13_diff",
        # "avg_ema_3_21_diff",
        # "avg_ema_5_8_diff",
        # "avg_ema_5_13_diff",
        # "avg_ema_5_21_diff",
        # "avg_ema_8_13_diff",
        # "avg_ema_8_21_diff",
        # "avg_ema_13_21_diff",
        # "ema_3_price_diff",
        # "ema_5_price_diff",
        # "ema_8_price_diff",
        # "ema_13_price_diff",
        # "ema_21_price_diff",
        "target"
    ]

    data_5m = df_5m[columns_to_keep]
    data_5m = candles.remove_outliers(data_5m, columns_to_keep)

    target = data_5m["target"]
    data_5m = data_5m.drop(["target"], axis=1)
    data_5m = scaler.scale(data_5m)
    data_5m["target"] = target

    data_5m.dropna(inplace=True)

    # d = dtale.show(data_5m, subprocess=False, host="localhost")
    # d.open_browser()

    print(data_5m.head(15))
    result = trainer.train(data_5m)

    # df_15m = scaler.scale(candles.resample_df(df_5m, '15min'))
    # df_30m = scaler.scale(candles.resample_df(df_5m, '30min'))
    # df_1h = scaler.scale(candles.resample_df(df_5m, '1h'))
    # df_2h = scaler.scale(candles.resample_df(df_5m, '2h'))
    # df_4h = scaler.scale(candles.resample_df(df_5m, '4h'))
    # df_1d = scaler.scale(candles.resample_df(df_5m, '1d'))

    # print(df_5m.head(15))
    # print(df_15m.head(15))
    # print(df_30m.head(15))
    # print(df_1h.head(15))
    # print(df_2h.head(15))
    # print(df_4h.head(15))
    # print(df_1d.head(15))


if __name__ == "__main__":
    main()
