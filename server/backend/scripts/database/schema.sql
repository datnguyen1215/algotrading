CREATE TABLE candles (
  id SERIAL PRIMARY KEY,
  symbol TEXT NOT NULL,
  time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
  open FLOAT NOT NULL,
  high FLOAT NOT NULL,
  low FLOAT NOT NULL,
  close FLOAT NOT NULL,
  UNIQUE (symbol, time, interval)
);

CREATE INDEX idx_candle_data_symbol ON candle_data(symbol);
CREATE INDEX idx_candle_data_time ON candle_data(time);