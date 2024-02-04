import pandas as pd


class CandleCollection:
    def __init__(self, tf_minute=5) -> None:
        self.tf_minute = tf_minute
        self.candles = pd.DataFrame()
        pass

    def add_candle(self, candle: pd.Series):
        candle = candle.copy()
        last_candle = self.last_candle()

        # in need of new candle
        #   1. no candles in collection
        #   2. last candle already closed
        if last_candle is None or (
            candle.name.minute % self.tf_minute == 0
            and candle.name.minute - last_candle.name.minute >= self.tf_minute
        ):
            candle.name = candle.name - pd.to_timedelta(
                candle.name.minute % self.tf_minute, unit="m"
            )
            self.candles = pd.concat([self.candles, candle.to_frame().T])
        # update last candle
        else:
            last_candle = last_candle.copy()
            last_candle["high"] = max(last_candle["high"], candle["high"])
            last_candle["low"] = min(last_candle["low"], candle["low"])
            last_candle["close"] = candle["close"]
            self.candles.iloc[-1] = last_candle
        pass

    def last_candle(self):
        try:
            return self.candles.iloc[-1]
        except IndexError:
            return None
