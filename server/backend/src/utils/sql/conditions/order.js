const order = (column, direction) => {
  if (!column || !direction) return '';

  return `${column} ${direction}`;
};

export default order;
