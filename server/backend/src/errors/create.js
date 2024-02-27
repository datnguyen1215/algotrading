class CustomError extends Error {
  /**
   *
   * @param {string} message
   * @param {object} extras
   * @param {number} extras.code
   * @param {string} extras.status
   */
  constructor(message, extras) {
    super(message);

    // copy all the extra properties to the error object
    for (const key in extras) this[key] = extras[key];
  }
}

/**
 * Create an error object that includes a code and a message
 * @param {string} message
 * @param {object} extras
 * @param {number} extras.code
 * @param {string} extras.status
 * @returns {CustomError}
 */
const create = (message, extras) => {
  return new CustomError(message, extras);
};

export default create;
