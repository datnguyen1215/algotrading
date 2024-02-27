import { Router } from 'express';
import candles from './candles';

const v1 = () => {
  const route = Router();

  route.use('/candles', candles());

  return route;
};

export default v1;
