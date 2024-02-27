import settings from '@src/settings';
import server from './server';
import api from './api';
import errors from '@src/errors';

let instance = server.create({
  host: settings.http.host,
  port: settings.http.port
});

/**
 * Start the HTTP server
 */
const start = async () => {
  try {
    instance.express.use('/api', api());
    await instance.start();
  } catch (err) {
    throw new errors.create(errors.codes.http.UNABLE_TO_START, err.message);
  }
};

/**
 * Stop the HTTP server
 */
const stop = async () => {
  try {
    await instance.stop();
  } catch (err) {
    throw new errors.create(errors.codes.http.UNABLE_TO_STOP, err.message);
  }
};

export default { start, stop };
