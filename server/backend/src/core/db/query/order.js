/**
 * Create order by query.
 * @param {QuerySortOption[]} options
 * @returns {string}
 */
const order = options => {
  if (!options) return '';

  // filter out empty options
  options = options.filter(x => x && x.column && x.by);

  const order = options.map(({ column, by }) => `${column} ${by}`);

  return `ORDER BY ${order.join(', ')}`;
};

export default order;
