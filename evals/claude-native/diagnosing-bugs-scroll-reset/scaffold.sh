#!/usr/bin/env bash
# G-01 fixture: selecting a creator rebuilds the list and resets its scroll position.
# The existing tests pass; none of them observes scroll position.
set -euo pipefail

export GIT_AUTHOR_DATE='2026-10-03T09:00:00+00:00' GIT_COMMITTER_DATE='2026-10-03T09:00:00+00:00'
git init -q -b main .
git config user.name 'Fixture Author'
git config user.email 'fixture@example.invalid'
git config core.hooksPath /dev/null
git config commit.gpgsign false

mkdir -p src test

cat > package.json <<'EOF'
{
  "name": "onboarding-fixture",
  "private": true,
  "type": "module",
  "scripts": {"test": "node --test"}
}
EOF

cat > src/onboarding.js <<'EOF'
// Creator picker state for mobile onboarding. The view renders `creators` in order
// and restores the list's scroll offset from `scrollTop` after every state change.

export function createState(creators) {
  return { creators, selected: [], scrollTop: 0, version: 0 };
}

export function scrollTo(state, top) {
  return { ...state, scrollTop: top };
}

export function selectCreator(state, id) {
  const selected = state.selected.includes(id)
    ? state.selected.filter((x) => x !== id)
    : [...state.selected, id];
  return reload({ ...state, selected });
}

// Rebuilds the list so selected creators sort first.
function reload(state) {
  const creators = [...state.creators].sort(
    (a, b) => Number(state.selected.includes(b.id)) - Number(state.selected.includes(a.id)),
  );
  return { ...state, creators, scrollTop: 0, version: state.version + 1 };
}
EOF

cat > test/onboarding.test.js <<'EOF'
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createState, selectCreator } from '../src/onboarding.js';

const creators = Array.from({ length: 30 }, (_, i) => ({ id: `c${i}`, name: `Creator ${i}` }));

test('selecting a creator marks it selected', () => {
  const state = selectCreator(createState(creators), 'c3');
  assert.deepEqual(state.selected, ['c3']);
});

test('selecting twice clears the selection', () => {
  const state = selectCreator(selectCreator(createState(creators), 'c3'), 'c3');
  assert.deepEqual(state.selected, []);
});
EOF

git add -A
git commit -q -m 'Creator picker for onboarding'
