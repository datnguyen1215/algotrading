import { Router } from 'express';
import candles from './candles';
import symbols from './symbols';

const v1 = () => {
  const route = Router();

  route.use('/candles', candles());
  route.use('/symbols', symbols());

  return route;
};

export default v1;
