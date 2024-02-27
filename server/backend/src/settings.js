import errors from './errors';

/**
 * Get the application settings
 * @returns {Settings}
 */
const get = () => {
  if (!process.env.DATABASE_CONNECTION_STRING)
    throw errors.create(
      errors.codes.database.MISSING_DATABASE_CONNECTION_STRING,
      'DATABASE_CONNECTION_STRING is not set'
    );

  if (!process.env.HTTP_PORT)
    throw errors.create(
      errors.codes.http.MISSING_HTTP_PORT,
      'HTTP_PORT is not set'
    );

  return {
    database: {
      connectionString: process.env.DATABASE_CONNECTION_STRING
    },
    http: {
      host: process.env.HTTP_HOST || 'localhost',
      port: process.env.HTTP_PORT || 3000
    }
  };
};

const settings = get();

export default settings;
