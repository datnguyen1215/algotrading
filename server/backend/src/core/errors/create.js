class CustomError extends Error {
  constructor(code, message) {
    super(message);
    this.code = code;
  }
}

/**
 * Create an error object that includes a code and a message
 * @param {number} code
 * @param {string} message
 * @returns
 */
const create = (code, message) => {
  return new CustomError(code, message);
};

export default create;
