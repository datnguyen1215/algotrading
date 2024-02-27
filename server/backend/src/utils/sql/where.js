/**
 * Create a WHERE clause from the given conditions. These conditions are already
 * joined with AND or OR operators.
 * @param  {string[]} args
 */
const where = (...args) => {
  const conditions = args.filter(x => !!x);

  if (conditions.length === 0) return '';

  return `WHERE ${conditions.join(' ')}`;
};

export default where;
