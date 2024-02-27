import assert from 'assert';
import where from '@src/utils/sql/where';

describe('src/utils/sql/where.js', () => {
  it('should have a where function', () => {
    assert(typeof where === 'function');
  });

  it('should return a string', () => {
    const result = where('a', 'b');
    assert(typeof result === 'string');
    assert(result.length > 0);
  });

  it('should return an empty string if no arguments are passed', () => {
    const result = where();
    assert(result === '');
  });

  it('should return an empty string if all arguments are falsy', () => {
    const result = where(null, undefined, '', 0, false);
    assert(result === '');
  });

  it('should return a single condition if only one is passed', () => {
    const result = where('a');
    assert(result === 'WHERE a');
  });

  it('should join multiple conditions with a space in between', () => {
    const result = where('a', 'b', 'c');
    assert(result === 'WHERE a b c');
  });
});
