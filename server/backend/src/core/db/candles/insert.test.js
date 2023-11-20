import assert from 'assert';
import insert from './insert';
import db from '@src/core/db';

describe('core/db/candles/insert', () => {
  describe('module exports', () => {
    it('should export a function', () => {
      assert.strictEqual(typeof insert, 'function');
    });
  });

  describe('insert()', () => {
    describe('insert a candle', () => {
      const candles = [
        {
          symbol: 'BTC/USD',
          time: '2021-01-01T10:20:30.400Z',
          open: 8000,
          close: 8000,
          high: 8000,
          low: 8000
        }
      ];

      /** @type {import('./insert').Candle[]} */
      let returnedData = [];

      it('should insert a candle', async () => {
        returnedData = await insert(candles);
      });

      it('returnedData should contain an array of candles', () => {
        const data = returnedData.map(({ id, ...rest }) => rest);
        assert.deepEqual(data, candles);
      });

      it('returnedData should include ids', () => {
        const data = returnedData.map(({ id }) => id);

        for (const id of data) {
          assert.strictEqual(typeof id, 'number');
        }
      });

      it('database should contain candle', async () => {
        const { rows } = await db.query.send(
          `SELECT * FROM candles WHERE symbol = '${candles[0].symbol}' AND time = '${candles[0].time}'`
        );

        const result = rows.map(x => ({ ...x, time: x.time.toISOString() }));

        assert.deepEqual(result, returnedData);
      });

      after(async () => {
        await db.query.send(
          `DELETE FROM candles WHERE id = ${returnedData[0].id}`
        );
      });
    });
  });
});
