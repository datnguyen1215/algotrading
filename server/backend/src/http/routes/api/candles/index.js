import { Router } from 'express';
import get from './get';

/**
 * Handle requests for /candles/*.
 * @returns {import('express').Router}
 */
const candles = () => {
  const router = Router();

  router.get('/', get());

  return router;
};

export default candles;
