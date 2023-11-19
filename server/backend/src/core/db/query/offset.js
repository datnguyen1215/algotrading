/**
 * Create offset query.
 * @param {number} offset
 * @returns
 */
const offset = offset => {
  if (!offset) return "";

  return `OFFSET ${offset}`;
};

export default offset;
