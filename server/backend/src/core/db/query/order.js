/**
 *
 * @param {QuerySortOption[]} options
 * @returns
 */

/**
 * Create order by query.
 * @returns
 */
const order = options => {
  if (!options || !options.length) return "";

  const order = options.map(({ column, by }) => `${column} ${by}`);
  return `ORDER BY ${order.join(", ")}`;
};

export default order;
