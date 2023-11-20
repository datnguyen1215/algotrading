/**
 * @typedef {object} CandleFilterOptions
 * @property {string} [symbol]
 * @property {number} [from]
 * @property {number} [to]
 * @property {number|string|Date} [time]
 */

/**
 * @typedef {object} GetCandlesOptions
 * @property {CandleFilterOptions} [filter]
 * @property {number} [limit]
 * @property {number} [offset]
 * @property {QuerySortOption[]} [sorts]
 */
import db from '@src/core/db';
import format from 'pg-format';

/**
 * Get candles from the database.
 * @param {GetCandlesOptions} options
 */
const get = async options => {
  if (!options) throw new Error('options is required.');

  const { filter = {}, limit = 100, offset = 0 } = options;
  const { symbol, from, to, time } = filter;

  const queryStr = format(
    `SELECT * FROM candles %s %s %s %s`,
    db.query.where(
      db.query.and(
        db.query.eq({
          column: 'symbol',
          value: symbol ? format('%L', symbol) : null
        }),
        db.query.ge({
          column: 'time',
          value: from ? format('%L', from) : null
        }),
        db.query.lt({ column: 'time', value: to ? format('%L', to) : null }),
        db.query.eq({ column: 'time', value: time ? format('%L', time) : null })
      )
    ),
    db.query.order([{ column: 'time', by: 'DESC' }]),
    db.query.limit(limit),
    db.query.offset(offset)
  );
  
  const { rows } = await db.query.send(queryStr);

  return rows.map(x => ({ ...x, time: x.time.toISOString() }));
};

export default get;
