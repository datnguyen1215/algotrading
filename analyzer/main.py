#!/usr/bin/python3
import pandas as pd
from preprocess import candles


def main():
    candles_df = candles.get()

    m5_collection = candles.CandleCollection(tf_minute=5)
    m15_collection = candles.CandleCollection(tf_minute=15)
    m30_collection = candles.CandleCollection(tf_minute=30)
    h1_collection = candles.CandleCollection(tf_minute=60)
    h4_collection = candles.CandleCollection(tf_minute=240)
    d1_collection = candles.CandleCollection(tf_minute=1440)

    for index in range(len(candles_df)):
        candle = candles_df.iloc[index]

        m5_collection.add_candle(candle)
        m15_collection.add_candle(candle)
        m30_collection.add_candle(candle)
        h1_collection.add_candle(candle)
        h4_collection.add_candle(candle)
        d1_collection.add_candle(candle)
    pass


if __name__ == "__main__":
    main()
