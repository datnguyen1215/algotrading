import { Router } from 'express';

const v1 = () => {
  const route = Router();

  route.get('/', (req, res) => {
    res.json({ message: 'Welcome to the API' });
  });

  return route;
};

export default v1;
