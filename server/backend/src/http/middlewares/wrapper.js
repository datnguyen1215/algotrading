import errors from '@src/errors';

const wrapper = fn => async (req, res, next) => {
  try {
    if (!fn)
      throw errors.create('Invalid function', {
        code: errors.codes.http.INVALID_FUNCTION,
        status: 500
      });

    await fn(req, res, next);
  } catch (err) {
    next(err);
  }
};

export default wrapper;
