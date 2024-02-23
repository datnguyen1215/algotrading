import settings from '@src/settings';
import http from './http';
import observability from './observability';

(async () => {
  observability.tracer.startActiveSpan('main', async span => {
    try {
      span.setAttributes({ settings });
      await http.start();
      span.end();
    } catch (error) {
      console.error(error);
    } finally {
      span.end();
    }
  });
})();
