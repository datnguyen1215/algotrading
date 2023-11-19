const Configuration = {
  postgres: {
    connectionString: process.env.DATABASE_URL
  },
  data: {
    candles: process.env.DATA_FILE
  }
};

export default Configuration;
