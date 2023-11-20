import express from 'express';
import http from 'http';
import routes from '../routes';
import CustomError from '@src/core/errors/custom';
import errors from '@src/core/errors';

/**
 * Start server.
 * @param {object} config
 * @param {number} config.port
 */
const start = async config => {
  return new Promise((resolve, reject) => {
    const app = express();

    app.use(express.json());
    app.use('/', routes());

    const server = http.createServer(app);

    server.listen(config.port, err => {
      if (err)
        return reject(
          new CustomError({
            message: err.message,
            stack: err.stack,
            code: errors.codes.HttpServer.START_ERROR
          })
        );

      resolve({
        http: server,
        express: app
      });
    });
  });
};

export default start;
