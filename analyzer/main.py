#!/usr/bin/python3
import candles

# get candles and plot
def main():
    df_5m = candles.get()
    df_15m = candles.resample_df(df_5m, '15min')
    df_30m = candles.resample_df(df_5m, '30min')
    df_1h = candles.resample_df(df_5m, '1h')
    df_2h = candles.resample_df(df_5m, '2h')
    df_4h = candles.resample_df(df_5m, '4h')
    df_1d = candles.resample_df(df_5m, '1d')
    print(df_5m.head(15))
    print(df_15m.head(15))
    print(df_30m.head(15))
    print(df_1h.head(15))
    print(df_2h.head(15))
    print(df_4h.head(15))
    print(df_1d.head(15))

if __name__ == "__main__":
    main()