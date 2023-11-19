/**
 * Create greater than or equal query.
 * @param {DbCompareOptions} options
 * @returns {string}
 */
const ge = options => {
  if (!options) return '';

  const { column, value } = options;

  if (!column || !value) return '';

  return `${column} > ${value}`;
};

export default ge;
