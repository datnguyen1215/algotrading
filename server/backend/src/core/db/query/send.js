import Configuration from '@src/configuration';
import errors from '@src/core/errors';
import pg from 'pg';

const pool = new pg.Pool({
  connectionString: Configuration.postgres.connectionString
});

/**
 * Send a query to the database.
 * @param {string} str
 * @returns {Promise<pg.QueryResult>}
 * @throws {CustomError}
 */
const send = async str => {
  try {
    return await pool.query(str);
  } catch (err) {
    throw errors.create({
      message: err.message,
      code: err.code,
      stack: err.stack
    });
  }
};

export default send;
