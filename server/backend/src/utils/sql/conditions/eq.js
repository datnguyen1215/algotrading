import errors from '@src/errors';

const eq = (column, value) => {
  if (!column)
    throw errors.create('column is required', {
      code: errors.codes.sql.INVALID_CONDITION
    });

  if (!value)
    throw errors.create('value is required', {
      code: errors.codes.sql.INVALID_CONDITION
    });

  return `${column} = ${value}`;
};

export default eq;
