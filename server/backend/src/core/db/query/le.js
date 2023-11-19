/**
 * Create LE query.
 * @param {DbCompareOptions} options
 * @returns {string}
 */
const le = options => {
  if (!options) return '';

  const { column, value } = options;
  if (!column || !value) return '';

  return `${column} <= ${value}`;
};

export default le;
