import pool from './pool';
import logging from '@src/logging';

const logger = logging.create('db');

/**
 * Send a query to the database
 * @param {string} str
 * @returns {Promise<import("pg").QueryResult<any>>}
 */
const query = async str => {
  logger.debug(`Database query: ${str}`);
  return await pool.query(str);
};

export default query;
