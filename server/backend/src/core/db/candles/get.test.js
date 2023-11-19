import format from 'pg-format';
import db from '@/core/db';
import candles from '.';
import assert from 'assert';

describe('core/db/candles/get', () => {
  describe('module exports', () => {
    it('should export a function', () => {
      assert.strictEqual(typeof candles.get, 'function');
    });
  });

  describe('get()', () => {
    const candleData = [
      {
        symbol: 'BTC/USD',
        time: '2021-01-01T10:20:30.400Z',
        open: 8000,
        close: 8000,
        high: 8000,
        low: 8000
      }
    ];

    before(async () => {
      await db.query.send(
        format(
          `INSERT INTO candles (symbol, time, open, close, high, low) VALUES %L`,
          candleData.map(({ symbol, time, open, close, high, low }) => [
            symbol,
            time,
            open,
            close,
            high,
            low
          ])
        )
      );
    });

    it('get a candle', async () => {
      const returnedData = await candles.get({
        filter: { symbol: 'BTC/USD', time: '2021-01-01T10:20:30.400Z' }
      });

      const data = returnedData.map(({ id, ...rest }) => rest);
      assert.deepEqual(data, candleData);
    });

    after(async () => {
      await db.query.send(
        format(
          `DELETE FROM candles WHERE symbol = '${candleData[0].symbol}' AND time = '${candleData[0].time}'`
        )
      );
    });
  });
});
