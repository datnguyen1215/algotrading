/**
 * Create limit query.
 * @param {number} limit
 * @returns {string}
 */
const limit = limit => {
  if (!limit) return '';

  return `LIMIT ${limit}`;
};

export default limit;
