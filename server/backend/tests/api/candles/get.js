import axios from 'axios';
import assert from 'assert';

describe('GET /api/candles', () => {
  it('no filter', async () => {
    const { data } = await axios.get('http://localhost:3005/api/candles');
    assert.ok(Array.isArray(data));
  });

  it('with limit', async () => {
    const { data } = await axios.get(
      'http://localhost:3005/api/candles?limit=10'
    );
    assert.ok(Array.isArray(data));
    assert.strictEqual(data.length, 10);
  });

  it('with offset', async () => {
    const { data } = await axios.get(
      'http://localhost:3005/api/candles?offset=10'
    );
    assert.ok(Array.isArray(data));
    assert.strictEqual(data.length, 100);
  });

  it('with filter time', async () => {
    const { data } = await axios.get(
      'http://localhost:3005/api/candles?filter[time]=2020-01-01T00:00:00.000Z'
    );
    assert.ok(Array.isArray(data));
    assert.strictEqual(data.length, 1);
  });

  it('with filter from', async () => {
    const { data } = await axios.get(
      'http://localhost:3005/api/candles?filter[from]=2020-01-01T00:00:00.000Z'
    );
    assert.ok(Array.isArray(data));
    assert.strictEqual(data.length, 100);
  });

  it('with filter to', async () => {
    const { data } = await axios.get(
      'http://localhost:3005/api/candles?filter[to]=2020-01-01T00:00:00.000Z'
    );
    assert.ok(Array.isArray(data));
    assert.strictEqual(data.length, 100);
  });

  it('with both filter from and to', async () => {
    const { data } = await axios.get(
      'http://localhost:3005/api/candles?filter[from]=2020-01-01T00:00:00.000Z&filter[to]=2020-02-01T00:00:00.000Z'
    );
    assert.ok(Array.isArray(data));
    assert.strictEqual(data.length, 100);
  });
});
