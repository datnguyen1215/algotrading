/**
 * @typedef {object} Candle
 * @property {string} symbol - the symbol of the asset
 * @property {number} time - the timestamp of the candle
 * @property {number} open - the opening price of the candle
 * @property {number} high - the highest price of the candle
 * @property {number} low - the lowest price of the candle
 * @property {number} close - the closing price of the candle
 */

/**
 * @typedef {object} Symbol
 * @property {string} name
 * @property {string} description
 */

/**
 * @typedef {object} Settings
 * @property {object} database
 * @property {string} database.connectionString
 * @property {object} http
 * @property {string} http.host
 * @property {number} http.port
 */
