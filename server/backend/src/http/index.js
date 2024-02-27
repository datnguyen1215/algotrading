import settings from '@src/settings';
import server from './server';
import api from './api';
import errors from '@src/errors';
import middlewares from './middlewares';
import logging from '@src/logging';

const logger = logging.create('http');

let instance = server.create({
  host: settings.http.host,
  port: settings.http.port
});

/**
 * Handle errors.
 */
const onError = (err, req, res, next) => {
  logger.error(err);
  res.status(err.status || 500).json({ message: err.message, code: err.code });
};

/**
 * Start the HTTP server
 */
const start = async () => {
  try {
    logger.info(`Configuring middlewares`);
    instance.express.use(middlewares.log());

    logger.info(`Configuring /api`);
    instance.express.use('/api', api());

    logger.info(`Configuring error handler`);
    instance.express.use(onError);

    logger.info(`Starting server...`);
    await instance.start();
    logger.info(`Server started at ${JSON.stringify(settings.http)}`);
  } catch (err) {
    throw new errors.create(err.message, {
      code: errors.codes.http.UNABLE_TO_START
    });
  }
};

/**
 * Stop the HTTP server
 */
const stop = async () => {
  try {
    logger.info(`Stopping server...`);
    await instance.stop();
    logger.info(`Server stopped`);
  } catch (err) {
    throw new errors.create(err.message, {
      code: errors.codes.http.UNABLE_TO_STOP
    });
  }
};

export default { start, stop };
