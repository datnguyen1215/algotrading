import axios from 'axios';
import settings from '@src/settings';
import errors from '@src/errors';
import chai from 'chai';
const { expect } = chai;

const base = `http://${settings.http.host}:${settings.http.port}`;
const url = `${base}/api/v1/candles`;

describe('GET /api/v1/candles', () => {
  it('should return 400 with invalid symbol', async () => {
    try {
      await axios.get(url);
    } catch (error) {
      expect(error.response.status).to.equal(400);
      expect(error.response.data.code).to.equal(
        errors.codes.http.INVALID_SYMBOL
      );
    }
  });

  it('should return 400 with invalid from', async () => {
    try {
      await axios.get(url, { params: { symbol: 'SYMBOLTEST' } });
    } catch (error) {
      expect(error.response.status).to.equal(400);
      expect(error.response.data.code).to.equal(errors.codes.http.INVALID_FROM);
    }
  });

  it('should return 400 with invalid interval', async () => {
    try {
      await axios.get(url, {
        params: { symbol: 'SYMBOLTEST', from: '2021-01-01' }
      });
    } catch (error) {
      expect(error.response.status).to.equal(400);
      expect(error.response.data.code).to.equal(
        errors.codes.http.INVALID_INTERVAL
      );
    }
  });

  it('should return 200 with limit', async () => {
    const query = {
      symbol: 'SYMBOLTEST',
      interval: 'm1',
      limit: 5,
      offset: 0,
      from: '2021-01-01T00:00:00.000Z',
      to: '2021-01-02T00:00:00.000Z'
    };

    const response = await axios.get(url, { params: query });

    expect(response.status).to.equal(200);
    expect(response.data.length).to.equal(5);
  });

  describe('Getting all available granularity data', () => {
    it('should get m1 data', async () => {
      const query = {
        symbol: 'SYMBOLTEST',
        interval: 'm1',
        limit: 10,
        offset: 0,
        from: '2021-01-01T00:00:00.000Z',
        to: '2021-01-02T00:00:00.000Z'
      };

      const response = await axios.get(url, { params: query });

      expect(response.status).to.equal(200);
      expect(response.data.length).to.equal(10);
    });

    it('should get m5 data', async () => {
      const query = {
        symbol: 'SYMBOLTEST',
        interval: 'm5',
        limit: 10,
        offset: 0,
        from: '2021-01-01T00:00:00.000Z',
        to: '2021-01-02T00:00:00.000Z'
      };

      const response = await axios.get(url, { params: query });

      expect(response.status).to.equal(200);
      expect(response.data.length).to.equal(10);
    });

    it('should get m15 data', async () => {
      const query = {
        symbol: 'SYMBOLTEST',
        interval: 'm15',
        limit: 10,
        offset: 0,
        from: '2021-01-01T00:00:00.000Z',
        to: '2021-01-02T00:00:00.000Z'
      };

      const response = await axios.get(url, { params: query });

      expect(response.status).to.equal(200);
      expect(response.data.length).to.equal(10);
    });

    it('should get m30 data', async () => {
      const query = {
        symbol: 'SYMBOLTEST',
        interval: 'm30',
        limit: 10,
        offset: 0,
        from: '2021-01-01T00:00:00.000Z',
        to: '2021-01-02T00:00:00.000Z'
      };

      const response = await axios.get(url, { params: query });

      expect(response.status).to.equal(200);
      expect(response.data.length).to.equal(10);
    });

    it('should get h1 data', async () => {
      const query = {
        symbol: 'SYMBOLTEST',
        interval: 'h1',
        limit: 10,
        offset: 0,
        from: '2021-01-01T00:00:00.000Z',
        to: '2021-01-15T00:00:00.000Z'
      };

      const response = await axios.get(url, { params: query });

      expect(response.status).to.equal(200);
      expect(response.data.length).to.equal(10);
    });

    it('should get h4 data', async () => {
      const query = {
        symbol: 'SYMBOLTEST',
        interval: 'h4',
        limit: 10,
        offset: 0,
        from: '2021-01-01T00:00:00.000Z',
        to: '2021-01-15T00:00:00.000Z'
      };

      const response = await axios.get(url, { params: query });

      expect(response.status).to.equal(200);
      expect(response.data.length).to.equal(10);
    });

    it('should get d1 data', async () => {
      const query = {
        symbol: 'SYMBOLTEST',
        interval: 'd1',
        limit: 10,
        offset: 0,
        from: '2021-01-01T00:00:00.000Z',
        to: '2021-01-15T00:00:00.000Z'
      };

      const response = await axios.get(url, { params: query });

      expect(response.status).to.equal(200);
      expect(response.data.length).to.equal(10);
      expect(response.data[0].time).to.equal('2021-01-01T00:00:00.000Z');
      expect(response.data[9].time).to.equal('2021-01-10T00:00:00.000Z');
    });
  });
});
