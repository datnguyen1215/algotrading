const order = (...args) => {
  const conditions = args.filter(x => !!x);

  if (conditions.length === 0) return '';

  return `ORDER BY ${conditions.join(', ')}`;
};

export default order;
