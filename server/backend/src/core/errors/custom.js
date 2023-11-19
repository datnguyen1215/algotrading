export default class CustomError extends Error {
  /**
   * @param {ErrorOptions} options
   */
  constructor(options) {
    super(options.message);
    this.code = options.code;
    this.stack = options.stack;
  }
}
