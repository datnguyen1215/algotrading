import db from '@src/db';
import format from 'pg-format';

/**
 * Add a candle to the database
 * @param {Candle} candles
 */
const add = async candles => {
  candles[0].created_time;
  const values = candles.map(candle => [
    candle.symbol,
    candle.time,
    candle.open,
    candle.high,
    candle.low,
    candle.close
  ]);

  const query = format(
    `
    INSERT INTO candles (symbol, time, open, high, low, close)
    VALUES %L
    ON CONFLICT DO NOTHING
    RETURNING *
    `,
    values
  );

  return await db.query(query);
};

export default add;
