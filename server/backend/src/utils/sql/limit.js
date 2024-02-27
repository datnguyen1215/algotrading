const limit = limit => {
  if (!limit) return '';

  return `LIMIT ${limit}`;
};

export default limit;
