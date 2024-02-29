/**
 * @typedef {Object} GetSymbolsQuery
 * @property {string} symbol
 */

import db from "@src/db";

/**
 * Extract the query from the request
 * @param {*} query
 * @returns {GetSymbolsQuery}
 */
const extractQuery = query => {
  const { symbol } = query;
  return { symbol };
};

const get = () => async (req, res) => {
  const params = extractQuery(req.query);

  const symbols = await db.symbols.get(params);

  res.status(200).json(symbols);
};

export default get;
