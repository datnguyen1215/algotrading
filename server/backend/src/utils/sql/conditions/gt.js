const gt = (column, value) => {
  if (!column)
    throw errors.create('Column is required', {
      code: errors.codes.sql.INVALID_CONDITION
    });

  if (!value) return '';

  return `${column} > ${value}`;
};

export default gt;
