import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createState, scrollTo, selectCreator } from '../src/onboarding.js';

const creators = Array.from({ length: 30 }, (_, i) => ({ id: `c${i}`, name: `Creator ${i}` }));

test('selecting a creator marks it selected', () => {
  const state = selectCreator(createState(creators), 'c3');
  assert.deepEqual(state.selected, ['c3']);
});

test('selecting twice clears the selection', () => {
  const state = selectCreator(selectCreator(createState(creators), 'c3'), 'c3');
  assert.deepEqual(state.selected, []);
});

test('selecting a creator keeps the list scroll position', () => {
  const scrolled = scrollTo(createState(creators), 492);
  const state = selectCreator(scrolled, 'c20');
  assert.equal(state.scrollTop, 492);
});
