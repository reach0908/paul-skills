#!/usr/bin/env bash
# S-01: a data-only change like a category merge. Only the server ingest mapping, its test
# and a migration change; no markup, style, token or user-facing string in src/ changes.
set -euo pipefail
source "$(dirname "$0")/../base.sh"

git switch -q -c feature/merge-ai-categories
export GIT_AUTHOR_DATE='2026-10-21T09:00:00+00:00' GIT_COMMITTER_DATE='2026-10-21T09:00:00+00:00'

cat > server/categories.ts <<'EOF'
// Canonical category slugs the ingest pipeline stores on articles.
export const CANONICAL = ['ai', 'design', 'infra', 'product'] as const;

// Source feeds use their own slugs; map them onto canonical ones.
const ALIASES: Record<string, string> = {
  'machine-learning': 'ai',
  'ai-tools': 'ai',
  llm: 'ai',
  ux: 'design',
  devops: 'infra',
};

export function normalizeCategory(slug: string): string {
  const key = slug.trim().toLowerCase();
  const target = ALIASES[key] ?? key;
  return (CANONICAL as readonly string[]).includes(target) ? target : 'other';
}
EOF

cat > server/categories.test.ts <<'EOF'
import { describe, expect, it } from 'vitest';
import { normalizeCategory } from './categories';

describe('normalizeCategory', () => {
  it('maps aliases onto canonical slugs', () => {
    expect(normalizeCategory('Machine-Learning')).toBe('ai');
    expect(normalizeCategory('ux')).toBe('design');
  });

  it('merges ai-tools and llm into ai', () => {
    expect(normalizeCategory('llm')).toBe('ai');
    expect(normalizeCategory('AI-Tools')).toBe('ai');
  });

  it('sends unknown slugs to other', () => {
    expect(normalizeCategory('gardening')).toBe('other');
  });
});
EOF

cat > server/migrations/0007_merge_ai_categories.sql <<'EOF'
-- ai-tools and llm are now aliases of ai.
UPDATE articles SET category = 'ai' WHERE category IN ('ai-tools', 'llm');
UPDATE categories SET hidden = TRUE WHERE slug IN ('ai-tools', 'llm');
EOF

git add -A
git commit -q -m 'Merge ai-tools and llm categories into ai' -m 'Both slugs now normalize to ai at ingest; the migration re-tags existing articles and hides the two old categories.'
