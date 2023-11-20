import '../alias';
import 'dotenv/config';
import Configuration from './configuration';
import http from './http';

(async () => {
  console.log('Starting HTTP server...');
  await http.server.start(Configuration.http);
  console.log(`HTTP Server started at port ${Configuration.http.port}`);
})();
