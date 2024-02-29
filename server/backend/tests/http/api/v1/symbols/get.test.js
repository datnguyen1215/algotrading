import settings from '@src/settings';
import axios from 'axios';
import { expect } from 'chai';

const base = `http://${settings.http.host}:${settings.http.port}`;
const url = `${base}/api/v1/symbols`;

describe('GET /api/v1/symbols', () => {
  it('should return a list of symbols', async () => {
    const { data } = await axios.get(url);
    expect(data).to.be.an('array');
    expect(data).to.have.lengthOf(1);
    expect(data[0]).to.have.property('name');
    expect(data[0]).to.have.property('description');
    expect(data[0].name).to.equal('SYMBOLTEST');
  });
});
