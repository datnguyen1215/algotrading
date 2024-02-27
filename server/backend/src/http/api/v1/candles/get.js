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
 *
 * @returns
 */
const get = () => async (req, res) => {
  const { symbol, interval, limit, offset, from, to } = extractQuery(req.query);

  if (!symbol)
    throw errors.create(`Invalid symbol: ${symbol}`, {
      code: errors.codes.http.INVALID_SYMBOL,
      status: 400
    });

  if (!from)
    throw errors.create(`Invalid from: ${from}`, {
      code: errors.codes.http.INVALID_FROM,
      status: 400
    });

  const tf_candle = db.candles[interval];

  if (!tf_candle)
    throw errors.create(`Invalid interval: ${interval}`, {
      code: errors.codes.http.INVALID_INTERVAL,
      status: 400
    });

  const candles = await tf_candle.get({
    symbol,
    limit,
    offset,
    from,
    to
  });

  res.json(candles);
};

export default get;
