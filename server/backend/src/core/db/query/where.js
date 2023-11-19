/**
 * Create WHERE query.
 * @param {string} str
 * @returns {string}
 */
const where = str => {
  if (!str) return '';

  return `WHERE ${str}`;
};

export default where;
