import assert from 'assert';
import and from '@src/utils/sql/and';

describe('src/utils/sql/and.js', () => {
  it('should have an and function', () => {
    assert(typeof and === 'function');
  });

  it('should return a string', () => {
    const result = and('a', 'b');
    assert(typeof result === 'string');
    assert(result.length > 0);
  });

  it('should return an empty string if no arguments are passed', () => {
    const result = and();
    assert(result === '');
  });

  it('should return an empty string if all arguments are falsy', () => {
    const result = and(null, undefined, '', 0, false);
    assert(result === '');
  });

  it('should return a single condition if only one is passed', () => {
    const result = and('a');
    assert(result === 'a');
  });

  it('should join multiple conditions with AND', () => {
    const result = and('a', 'b', 'c');
    assert(result === 'a AND b AND c');
  });
});
