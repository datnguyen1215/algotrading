const Configuration = {
  postgres: {
    connectionString: process.env.DATABASE_URL
  },
  data: {
    candles: process.env.DATA_FILE,
    symbol: process.env.SYMBOL
  },
  http: {
    port: parseInt(process.env.HTTP_PORT)
  }
};

export default Configuration;
