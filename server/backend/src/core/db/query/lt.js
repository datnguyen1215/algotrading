/**
 * Create less than query.
 * @param {DbCompareOptions} options
 * @returns {string}
 */
const lt = options => {
  if (!options) return '';

  const { column, value } = options;

  if (!column || !value) return '';

  return `${column} < ${value}`;
};

export default lt;
