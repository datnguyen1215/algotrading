/**
 * @typedef {object} GetCandleQuery
 * @property {string} symbol
 * @property {'m1'|'m5'|'m15'|'m30'|'h1'|'h4'|'d1'} interval
 * @property {number} limit
 * @property {number} offset
 * @property {string} from
 * @property {string} to
 */

import db from '@src/db';
import errors from '@src/errors';

/**
 * @param {*} query
 * @returns {GetCandleQuery}
 */
const extractQuery = query => {
  return {
    symbol: query.symbol,
    interval: query.interval,
    limit: query.limit,
    offset: query.offset,
    from: query.from,
    to: query.to
  };
};

/**
 * Create GET /api/v1/candles handler.
 */
const get = () => async (req, res) => {
  const { symbol, interval, limit, offset, from, to } = extractQuery(req.query);

  const candles = await db.candles.get({
    symbol,
    interval,
    limit,
    offset,
    from,
    to
  });

  res.json(candles);
};

export default get;
