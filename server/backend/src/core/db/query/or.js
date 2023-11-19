/**
 * Create OR query.
 * @param {...string} args
 * @returns {string}
 */
const or = (...args) => {
  if (!args || args.length === 0) return '';

  return `(${args.join(' OR ')})`;
};

export default or;
