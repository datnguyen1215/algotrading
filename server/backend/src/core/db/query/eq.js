/**
 * Create equal query.
 * @param {DbCompareOptions} options
 * @returns {string}
 */
const eq = options => {
  if (!options) return '';

  const { column, value } = options;

  if (!column || !value) return '';

  return `${column} = ${value}`;
};

export default eq;
