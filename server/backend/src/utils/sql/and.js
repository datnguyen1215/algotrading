/**
 * Join the given conditions with AND
 * @param  {string[]} args
 * @returns
 */
const and = (...args) => {
  const conditions = args.filter(x => !!x);

  if (conditions.length === 0) return '';

  return conditions.join(' AND ');
};

export default and;
