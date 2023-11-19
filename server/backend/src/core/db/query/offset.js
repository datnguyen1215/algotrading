/**
 * Create offset query.
 * @param {number} offset
 * @returns {string}
 */
const offset = offset => {
  if (!offset) return '';

  return `OFFSET ${offset}`;
};

export default offset;
