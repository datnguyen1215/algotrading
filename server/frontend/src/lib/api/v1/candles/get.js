/**
 * @typedef {object} GetCandlesOptions
 * @property {string} symbol - the symbol of the asset
 * @property {string} [from] - the start timestamp
 * @property {string} [to] - the end timestamp
 * @property {'m1'|'m5'|'m15'|'m30'|'h1'|'h4'|'d1'} interval - the interval of the candles
 * @property {number} [limit] - the maximum number of candles to return
 * @property {number} [offset] - the number of candles to skip
 */
import axios from 'axios';

/**
 * @param {GetCandlesOptions} options
 * @returns {Promise<Candle[]>}
 */
const get = async options => {
  const { symbol, from, to, interval, limit, offset } = options;

  const response = await axios.get(`/api/v1/candles`, {
    params: {
      symbol,
      from,
      to,
      interval,
      limit,
      offset
    }
  });

  return response.data;
};

export default get;
