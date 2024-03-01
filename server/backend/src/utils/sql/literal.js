import format from 'pg-format';

/**
 * Put a string in a format that is safe to use in a SQL query.
 * @param {string} value
 * @returns {string}
 */
const literal = value => {
  if (!value) return '';

  return format('%L', value);
};

export default literal;
