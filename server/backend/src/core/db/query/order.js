/**
 * Create order by query.
 * @param {QuerySortOption[]} options
 * @returns {string}
 */
const order = options => {
  if (!options || !options.length) return '';

  const order = options.map(({ column, by }) => {
    if (!column || !by) return '';

    return `${column} ${by}`;
  });

  return `ORDER BY ${order.join(', ')}`;
};

export default order;
