/**
 * Join the given conditions with OR
 * @param  {string[]} args
 * @returns
 */
const or = (...args) => {
  const conditions = args.filter(x => !!x);

  if (conditions.length === 0) return '';

  return conditions.join(' OR ');
};

export default or;
