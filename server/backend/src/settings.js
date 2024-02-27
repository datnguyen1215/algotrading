import errors from './errors';

/**
 * Get the application settings
 * @returns {Settings}
 */
const get = () => {
  if (!process.env.DATABASE_CONNECTION_STRING)
    throw errors.create('DATABASE_CONNECTION_STRING is not set', {
      code: errors.codes.database.MISSING_DATABASE_CONNECTION_STRING
    });

  if (!process.env.HTTP_PORT)
    throw errors.create('HTTP_PORT is not set', {
      code: errors.codes.http.MISSING_HTTP_PORT
    });

  return {
    database: {
      connectionString: process.env.DATABASE_CONNECTION_STRING
    },
    http: {
      host: process.env.HTTP_HOST || 'localhost',
      port: process.env.HTTP_PORT || 3000
    },
    logging: {
      level: process.env.LOGGING_LEVEL || 'info'
    }
  };
};

const settings = get();

export default settings;
