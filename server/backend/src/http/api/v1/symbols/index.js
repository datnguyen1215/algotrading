import { Router } from 'express';
import get from './get';
import middlewares from '@src/http/middlewares';

const symbols = () => {
  const route = Router();

  route.get('/', middlewares.wrapper(get()));

  return route;
};

export default symbols;
