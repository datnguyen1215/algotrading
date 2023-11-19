import Configuration from "@/configuration";
import db from "pg";

const pool = new db.Pool({
  connectionString: Configuration.postgres.connectionString
});

/**
 * Send a query to the database.
 * @param {string} str
 * @returns {Promise<db.QueryResult>}
 */
const send = async str => await pool.query(str);

export default send;
