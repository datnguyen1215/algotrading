import assert from 'assert';
import or from '@src/utils/sql/or';

describe('src/utils/sql/or.js', () => {
  it('should have an or function', () => {
    assert(typeof or === 'function');
  });

  it('should return a string', () => {
    const result = or('a', 'b');
    assert(typeof result === 'string');
    assert(result.length > 0);
  });

  it('should return an empty string if no arguments are passed', () => {
    const result = or();
    assert(result === '');
  });

  it('should return an empty string if all arguments are falsy', () => {
    const result = or(null, undefined, '', 0, false);
    assert(result === '');
  });

  it('should return a single condition if only one is passed', () => {
    const result = or('a');
    assert(result === 'a');
  });

  it('should join multiple conditions with OR', () => {
    const result = or('a', 'b', 'c');
    assert(result === 'a OR b OR c', result);
  });
});
