import format from 'pg-format';
import sql from '@src/utils/sql';
import db from '@src/db';

/**
 * Get M1 candles.
 * @param {*} options
 * @returns {Promise<Candle[]>}
 */
const get = async options => {
  const { symbol, from, to, limit, offset } = options;

  const where = sql.where(
    sql.and(
      sql.conditions.eq('symbol', format('%L', symbol)),
      sql.conditions.ge('time', format('%L', from)),
      sql.conditions.le('time', format('%L', to))
    )
  );

  const orders = sql.order(sql.conditions.order('time', 'ASC'));

  const query = format(
    `SELECT * FROM candles_m1 %s %s %s %s `,
    where,
    orders,
    sql.limit(limit),
    sql.offset(offset)
  );

  return (await db.query(query)).rows;
};

export default get;
