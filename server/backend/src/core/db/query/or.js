/**
 * Create OR query.
 * @param {...string} args
 * @returns {string}
 */
const or = (...args) => {
  if (!args) return '';

  // filter out empty args.
  args = args.filter(x => x);

  if (!args.length) return '';

  return `(${args.join(' OR ')})`;
};

export default or;
