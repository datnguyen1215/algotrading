/**
 * Create limit query.
 * @param {number} limit
 * @returns
 */
const limit = limit => {
  if (!limit) return "";

  return `LIMIT ${limit}`;
};

export default limit;
