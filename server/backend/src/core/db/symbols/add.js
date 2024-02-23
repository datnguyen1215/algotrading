import db from '@src/db';
import format from 'pg-format';

/**
 * Add a symbol to the database.
 * @param {Symbol} symbol
 */
const add = async symbol => {
  // on conflict, update description
  const query = format(
    `
    INSERT INTO symbols (name, description)
    VALUES (%L, %L)
    ON CONFLICT (name)
    DO UPDATE SET description = EXCLUDED.description
    `,
    symbol.name,
    symbol.description
  );

  return await db.query(query);
};

export default add;
