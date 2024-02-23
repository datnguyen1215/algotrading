import { Router } from 'express';
import v1 from './v1';

const api = () => {
  const app = Router();

  app.use('/v1', v1());

  return app;
};

export default api;
