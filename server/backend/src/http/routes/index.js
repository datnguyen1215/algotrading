import { Router } from 'express';
import api from './api';

/**
 * Handle requests for /.
 * @returns {import('express').Router}
 */
const routes = () => {
  const router = Router();

  router.use('/api', api());

  return router;
};

export default routes;
