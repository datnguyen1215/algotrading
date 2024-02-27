import settings from '@src/settings';
import http from './http';

(async () => {
  try {
    await http.start();
  } catch (error) {
    console.error(error);
    process.exit(1);
  }
})();
