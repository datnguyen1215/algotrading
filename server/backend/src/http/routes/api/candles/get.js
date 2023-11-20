import db from '@/src/core/db';

/**
 * Handle GET request for candles.
 * @returns {import('express').RequestHandler}
 */
const get = () => async (req, res) => {
  const candles = await db.candles.get(req.query);

  // id has no need to be in the returned data.
  candles.forEach(x => delete x.id);

  res.json(candles);
};

export default get;
