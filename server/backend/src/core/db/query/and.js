/**
 * Create AND query.
 * @param  {...string} args
 * @returns {string}
 */
const and = (...args) => {
  if (!args || args.length === 0) return '';

  return `(${args.filter(x => x).join(' AND ')})`;
};

export default and;
