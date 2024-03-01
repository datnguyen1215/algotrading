/**
 * @typedef {object} Symbol
 * @property {string} symbol
 * @property {string} name
 */
import axios from 'axios';

/**
 * Get all symbols.
 * @returns {Promise<Symbol[]>}
 */
const get = async () => {
  const result = await axios.get('/api/v1/symbols');
  return result.data;
};

export default get;
