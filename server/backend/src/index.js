import 'dotenv/config'
import './aliases';
import settings from '@src/settings';
import http from './http';
import logging from './logging';

const logger = logging.create('index');

(async () => {
  try {
    logger.info(`Settings: ${JSON.stringify(settings)}`);
    await http.start();
  } catch (error) {
    console.error(error);
    process.exit(1);
  }
})();
