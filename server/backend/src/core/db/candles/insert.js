/**
 * @typedef {object} Candle
 * @property {number|string} [id]
 * @property {string} symbol
 * @property {number} open
 * @property {number} high
 * @property {number} low
 * @property {number} close
 * @property {string|number} time
 */
import db from '@/core/db';
import format from 'pg-format';

/**
 * Insert candle data into the database.
 * @param {Candle[]} data
 * @returns {Promise<Candle[]>}
 */
const insert = async data => {
  const values = data.map(({ symbol, time, open, high, low, close }) => [
    symbol,
    time,
    open,
    high,
    low,
    close
  ]);

  // there's no need to collect any data
  const { rows } = await db.query.send(
    format(
      `INSERT INTO candles (symbol, time, open, high, low, close) VALUES %L RETURNING *`,
      values
    )
  );

  return rows.map(x => ({ ...x, time: x.time.toISOString() }));
};

export default insert;
