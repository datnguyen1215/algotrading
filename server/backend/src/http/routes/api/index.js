import { Router } from 'express';
import candles from './candles';

/**
 * Handle requests for /api/*.
 */
const api = () => {
  const router = Router();

  router.use('/candles', candles());

  return router;
};

export default api;