import format from 'date-format';

const timestamp = options => ({
  ...options,
  timestamp: format('yyyy-MM-dd hh:mm:ss', new Date())
});

export default timestamp;
