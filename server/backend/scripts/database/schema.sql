CREATE TABLE candles (
  id SERIAL PRIMARY KEY,
  symbol TEXT NOT NULL,
  time TIMESTAMPTZ NOT NULL,
  open FLOAT NOT NULL,
  high FLOAT NOT NULL,
  low FLOAT NOT NULL,
  close FLOAT NOT NULL,
  UNIQUE (symbol, time)
);

CREATE INDEX idx_candles_symbol ON candles(symbol);
CREATE INDEX idx_candles_time ON candles(time);