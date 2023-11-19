import CustomError from "./custom";

/**
 * Create an error
 * @param {ErrorOptions} options
 * @returns {CustomError}
 */
const create = (options) => new CustomError(options);

export default create;
