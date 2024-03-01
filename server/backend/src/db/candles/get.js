import format from 'pg-format';
import sql from '@src/utils/sql';
import db from '@src/db';
import errors from '@src/errors';

const GRANULARITY_MAP = {
  m1: 'candles_m1',
  m5: 'candles_m5',
  m15: 'candles_m15',
  m30: 'candles_m30',
  h1: 'candles_h1',
  h4: 'candles_h4',
  d1: 'candles_d1'
};

/**
 * Get M1 candles.
 * @param {object} options
 * @param {string} options.symbol
 * @param {'m1'|'m5'|'m15'|'m30'|'h1'|'h4'|'d1'} options.interval
 * @param {string} options.from
 * @param {string} options.to
 * @param {number} options.limit
 * @param {number} options.offset
 * @returns {Promise<Candle[]>}
 */
const get = async options => {
  const { symbol, interval, from, to, limit, offset } = options;

  if (!symbol)
    throw errors.create(`Invalid symbol: ${symbol}`, {
      code: errors.codes.options.INVALID_SYMBOL,
      status: 400
    });

  if (!from)
    throw errors.create(`Invalid from: ${from}`, {
      code: errors.codes.options.INVALID_FROM,
      status: 400
    });

  if (!interval)
    throw errors.create(`Invalid interval: ${interval}`, {
      code: errors.codes.options.INVALID_INTERVAL,
      status: 400
    });

  const table = GRANULARITY_MAP[interval];

  if (!table)
    throw errors.create(`Invalid interval: ${interval}`, {
      code: errors.codes.options.INVALID_INTERVAL,
      status: 400
    });

  const where = sql.where(
    sql.and(
      sql.conditions.eq('symbol', sql.literal(symbol)),
      sql.conditions.ge('time', sql.literal(from)),
      sql.conditions.le('time', sql.literal(to))
    )
  );

  const orders = sql.order(sql.conditions.order('time', 'ASC'));

  const query = format(
    `SELECT * FROM %s %s %s %s %s `,
    table,
    where,
    orders,
    sql.limit(limit),
    sql.offset(offset)
  );

  return (await db.query(query)).rows;
};

export default get;
