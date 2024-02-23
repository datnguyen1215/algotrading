/**
 * @typedef {object} Candle
 * @property {string} symbol - the symbol of the asset
 * @property {number} time - the timestamp of the candle
 * @property {number} open - the opening price of the candle
 * @property {number} high - the highest price of the candle
 * @property {number} low - the lowest price of the candle
 * @property {number} close - the closing price of the candle
 */

import db from '@src/db';
import format from 'pg-format';

/**
 * Add a candle to the database
 * @param {CandleWithTimestamp[]} candles
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
