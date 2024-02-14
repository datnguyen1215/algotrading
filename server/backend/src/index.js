import 'dotenv/config';
import './aliases';
import http from './http';

(async () => {
  await http.start();
  await http.stop();
})();
