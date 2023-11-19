/**
 * Create greater than query.
 * @param {DbCompareOptions} options
 * @returns {string}
 */
const gt = options => {
  if (!options) return '';

  const { column, value } = options;

  if (!column || !value) return '';

  return `${column} > ${value}`;
};

export default gt;
