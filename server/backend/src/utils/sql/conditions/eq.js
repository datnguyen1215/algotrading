import errors from '@src/errors';

const eq = (column, value) => {
  if (!column)
    throw errors.create('column is required', {
      code: errors.codes.sql.INVALID_CONDITION
    });

  if (!value || value == 'NULL') return '';

  return `${column} = ${value}`;
};

export default eq;
