import settings from '@src/settings';
import server from './server';
import api from './api';
import errors from '@src/errors';
import observability from '@src/observability';

let instance = server.create({
  host: settings.http.host,
  port: settings.http.port
});

/**
 * Start the HTTP server
 */
const start = async () => {
  return observability.tracer.startActiveSpan('http.start', async span => {
    try {
      span.addEvent('instance.express.use', 'api');
      instance.express.use('/api', api());

      span.addEvent('instance.start');
      await instance.start();
      span.end();
    } catch (err) {
      throw new errors.create(errors.codes.http.UNABLE_TO_START, err.message);
    }
  });
};

/**
 * Stop the HTTP server
 */
const stop = async () => {
  return observability.tracer.startActiveSpan('http.stop', async span => {
    try {
      span.addEvent('instance.stop');
      await instance.stop();
      span.end();
    } catch (err) {
      throw new errors.create(errors.codes.http.UNABLE_TO_STOP, err.message);
    }
  });
};

export default { start, stop };
