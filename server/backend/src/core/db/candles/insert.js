/**
 * @typedef {object} Candle
 * @property {number} open
 * @property {number} high
 * @property {number} low
 * @property {number} close
 * @property {number} time
 */
import db from "@/core/db";
import format from "pg-format";

/**
 * Insert candle data into the database.
 * @param {Candle[]} data
 * @returns {Promise<QueryResult>}
 */
const insert = async data => {
  try {
    const values = data.map(({ time, open, high, low, close }) => [
      time,
      open,
      high,
      low,
      close
    ]);

    const res = await db.query(
      format(
        `INSERT INTO candles (time, open, high, low, close) VALUES %L`,
        values
      )
    );

    // if everything is good, just return the data.
    return { data };
  } catch (error) {
    return { error };
  }
};

export default insert;
