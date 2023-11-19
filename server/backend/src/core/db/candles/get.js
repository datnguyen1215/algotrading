/**
 * @typedef {object} CandleFilterOptions
 * @property {string} [symbol]
 * @property {number} [from]
 * @property {number} [to]
 */

/**
 * @typedef {object} GetCandlesOptions
 * @property {CandleFilterOptions} [filter]
 * @property {number} [limit]
 * @property {number} [offset]
 * @property {QuerySortOption[]} [sorts]
 */
import db from "@/core/db";

/**
 *
 * @param {GetCandlesOptions} options
 */
const get = options => {
  const { filter = {}, limit = 100, offset = 0 } = options;
  const { symbol, from, to } = filter;

  const query = `
    SELECT symbol, time, open, high, low, close
    FROM candles
    WHERE symbol = $1 AND date >= $2 AND date <= $3
    ORDER BY date ASC
    LIMIT $4 OFFSET $5
  `;
};
