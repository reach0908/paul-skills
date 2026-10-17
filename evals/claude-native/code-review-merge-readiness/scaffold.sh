#!/usr/bin/env bash
# K-01 fixture: a feature branch with one standards violation (fractional cents), one spec
# gap (case-insensitive codes) and a README conflict with a later main commit. HEAD is on
# the feature branch with a clean working tree. Self-contained; fixed dates keep SHAs stable.
set -euo pipefail

commit_at() {
  GIT_AUTHOR_DATE="$1" GIT_COMMITTER_DATE="$1" git commit -q -m "$2"
}

git init -q -b main .
git config user.name 'Fixture Author'
git config user.email 'fixture@example.invalid'
git config core.hooksPath /dev/null
git config commit.gpgsign false

mkdir -p src test docs/specs

cat > package.json <<'EOF'
{
  "name": "cart-fixture",
  "private": true,
  "type": "module",
  "scripts": {"test": "node --test"}
}
EOF

cat > CODING_STANDARDS.md <<'EOF'
# Coding standards

1. Money is integer cents everywhere. Never produce a fractional amount; round down with `Math.floor` where a percentage is applied.
2. Every exported function has tests under `test/`.
3. Name modules after the domain concept they hold.
EOF

cat > README.md <<'EOF'
# Cart

Checkout helpers for the shop.

## Features

- Subtotals in integer cents
EOF

cat > src/cart.js <<'EOF'
// Money is integer cents throughout (see CODING_STANDARDS.md).
export function subtotalCents(items) {
  return items.reduce((sum, item) => sum + item.priceCents * item.quantity, 0);
}
EOF

cat > test/cart.test.js <<'EOF'
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { subtotalCents } from '../src/cart.js';

test('subtotal sums price times quantity in cents', () => {
  assert.equal(subtotalCents([{ priceCents: 250, quantity: 2 }, { priceCents: 100, quantity: 1 }]), 600);
});
EOF

cat > docs/specs/discount-codes.md <<'EOF'
# Discount codes (#12)

Add `applyDiscount(totalCents, code)` to `src/discount.js`.

1. Returns the discounted total in cents.
2. `SAVE10` takes 10% off. `FLAT500` takes 500 cents off.
3. An unknown code throws `RangeError`.
4. The total never goes below 0.
5. Codes are case-insensitive: `save10` works like `SAVE10`.
EOF

git add -A
commit_at '2026-10-05T09:00:00+00:00' 'Add cart subtotals'

git switch -q -c feature/discount-codes

cat > src/discount.js <<'EOF'
const CODES = {
  SAVE10: (totalCents) => totalCents * 0.9,
  FLAT500: (totalCents) => totalCents - 500,
};

export function applyDiscount(totalCents, code) {
  const discount = CODES[code];
  if (!discount) throw new RangeError(`Unknown discount code: ${code}`);
  return Math.max(0, discount(totalCents));
}
EOF

cat > test/discount.test.js <<'EOF'
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { applyDiscount } from '../src/discount.js';

test('SAVE10 takes 10% off', () => {
  assert.equal(applyDiscount(1000, 'SAVE10'), 900);
});

test('FLAT500 takes 500 cents off and never goes below zero', () => {
  assert.equal(applyDiscount(1000, 'FLAT500'), 500);
  assert.equal(applyDiscount(300, 'FLAT500'), 0);
});

test('unknown codes are rejected', () => {
  assert.throws(() => applyDiscount(1000, 'BOGUS'), RangeError);
});
EOF

printf -- '- Discount codes (#12)\n' >> README.md
git add -A
commit_at '2026-10-06T09:00:00+00:00' 'Add discount codes (#12)'

git switch -q main
printf -- '- Gift cards (#14)\n' >> README.md
git add README.md
commit_at '2026-10-07T09:00:00+00:00' 'Document gift cards (#14)'

git switch -q feature/discount-codes
