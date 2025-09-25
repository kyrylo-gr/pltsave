// math.test.ts
import { add, multiply } from './math';

test('adds 1 + 2 to equal 3', () => {
  expect(add(2, 2)).toBe(4);
});

test('multiplies 2 * 3 to equal 6', () => {
  expect(multiply(2, 3)).toBe(6);
});
