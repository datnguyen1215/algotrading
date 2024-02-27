import logging from '@src/logging';

const logger = logging.create('http/middlewares/log.js');

const log = () => (req, res, next) => {
  logger.info(`${req.method} ${req.originalUrl}`);
  next();
};

export default log;
