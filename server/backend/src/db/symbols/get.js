import db from '..';
import format from 'pg-format';
import sql from '@src/utils/sql';

const get = async options => {
  const conditions = sql.where(
    sql.conditions.eq('name', sql.literal(options.symbol))
  );

  const query = format('SELECT * FROM symbols %s', conditions);

  const result = await db.query(query);

  return result.rows;
};

export default get;
