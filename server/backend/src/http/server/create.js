/**
 * @typedef {object} HttpConfig
 * @property {number} port
 * @property {string} host
 */

import http from 'http';
import express from 'express';

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
    return new Promise((resolve, reject) => {
      server.listen(config.port, config.host, err => {
        if (err) {
          reject(err);
          return;
        }

        resolve();
      });
    });
  };

  /**
   * Stop the HTTP server
   * @returns {Promise<void>}
   */
  const stop = async () => {
    return new Promise((resolve, reject) => {
      server.close(err => {
        if (err) {
          reject(err);
          return;
        }

        resolve();
      });
    });
  };

  return {
    express: app,
    http: server,
    start,
    stop
  };
};

export default create;
