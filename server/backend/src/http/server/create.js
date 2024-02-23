/**
 * @typedef {object} HttpConfig
 * @property {number} port
 * @property {string} host
 */

import http from 'http';
import express from 'express';
import observability from '@src/observability';
import utils from '@src/utils';

/**
 * Create an HTTP server
 * @param {HttpConfig} config
 */
const create = config => {
  let app = express();
  let server = http.createServer(app);

  /**
   * Start the HTTP server
   * @returns {Promise<void>}
   */
  const start = async () => {
    return observability.tracer.startActiveSpan(
      'http.server.create.start',
      async span => {
        return new Promise((resolve, reject) => {
          span.setAttributes(utils.flatten({ config }));
          server.listen(config.port, config.host, err => {
            if (err) {
              span.addEvent('server.error', {
                message: err.message,
                stack: err.stack
              });
              span.end();
              reject(err);
              return;
            }

            span.addEvent('server.listening');
            resolve();
            span.end();
          });
        });
      }
    );
  };

  /**
   * Stop the HTTP server
   * @returns {Promise<void>}
   */
  const stop = async () => {
    return observability.tracer.startActiveSpan(
      'http.server.create.stop',
      async span => {
        return new Promise((resolve, reject) => {
          server.close(err => {
            if (err) {
              span.addEvent('server.error', {
                message: err.message,
                stack: err.stack
              });
              reject(err);
              span.end();
              return;
            }

            span.addEvent('server.closed');
            span.end();
            resolve();
          });
        });
      }
    );
  };

  return {
    express: app,
    http: server,
    start,
    stop
  };
};

export default create;
