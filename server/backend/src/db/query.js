import pool from "./pool";

/**
 * Send a query to the database
 * @param {string} str
 * @returns {Promise<import("pg").QueryResult<any>>}
 */
const query = async str => await pool.query(str);

export default query;
