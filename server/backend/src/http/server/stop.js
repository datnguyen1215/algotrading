/**
 * Stop HTTP server.
 * @param {import('http').Server} server
 * @returns
 */
const stop = server => {
  return new Promise((resolve, reject) => {
    server.close(err => {
      if (err) return reject(err);

      resolve();
    });
  });
};

export default stop;
