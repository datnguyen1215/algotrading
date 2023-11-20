/**
 * Create AND query.
 * @param  {...string} args
 * @returns {string}
 */
const and = (...args) => {
  if (!args) return '';

  // filter out empty args.
  args = args.filter(x => x);

  if (!args.length) return '';

  return `(${args.filter(x => x).join(' AND ')})`;
};

export default and;
