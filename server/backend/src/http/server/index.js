import startServer from './start';
import stopServer from './stop';

let server = {
  /** @type {import('http').Server} */
  http: null,
  /** @type {import('express').Application} */
  express: null
};

/**
 * Start HTTP Server.
 * @param {object} config
 * @param {number} config.port
 */
const start = async config => {
  if (server.http) return;

  server = await startServer(config);
};

/**
 * Stop HttpServer
 */
const stop = async () => {
  if (!server.http) return;

  await stopServer(server.http);

  // reset the state of the server.
  server = { http: null, express: null };
};

export { start, stop };
export default { start, stop };
