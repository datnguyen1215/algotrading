import loglevel from 'loglevel';
import format from './format';
import timestamp from './timestamp';

const create = name => {
  const logger = loglevel.getLogger(name);
  logger.setLevel('info');

  const debug = (...args) =>
    logger.debug(
      format(timestamp({ level: 'debug', label: name, messages: args }))
    );

  const info = (...args) =>
    logger.info(
      format(timestamp({ level: 'info', label: name, messages: args }))
    );

  const error = (...args) =>
    logger.error(
      format(timestamp({ level: 'error', label: name, messages: args }))
    );

  const warn = (...args) =>
    logger.warn(
      format(timestamp({ level: 'warn', label: name, messages: args }))
    );

  return { debug, info, warn, error };
};

export default create;
