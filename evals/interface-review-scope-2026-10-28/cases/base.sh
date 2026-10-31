#!/usr/bin/env bash
# Shared synthetic fixture for the interface-review scope trial: a small React feed app
# with a Node API, committed on main. Each case's scaffold.sh sources this file, switches
# to a feature branch and commits one change. No private code; all names are invented.
set -euo pipefail

export GIT_AUTHOR_DATE='2026-10-20T09:00:00+00:00' GIT_COMMITTER_DATE='2026-10-20T09:00:00+00:00'
git init -q -b main .
git config user.name 'Fixture Author'
git config user.email 'fixture@example.invalid'
git config core.hooksPath /dev/null
git config commit.gpgsign false

mkdir -p src/styles src/components src/pages src/api server/migrations

cat > package.json <<'EOF'
{
  "name": "signal-feed-fixture",
  "private": true,
  "type": "module",
  "scripts": { "dev": "vite", "test": "vitest run" },
  "dependencies": { "react": "18.3.1", "react-dom": "18.3.1" },
  "devDependencies": { "typescript": "5.6.3", "vite": "5.4.10", "vitest": "2.1.4" }
}
EOF

cat > pnpm-lock.yaml <<'EOF'
lockfileVersion: '9.0'
importers:
  .:
    dependencies:
      react:
        specifier: 18.3.1
        version: 18.3.1
EOF

cat > src/styles/tokens.css <<'EOF'
:root {
  --color-text: #111827;
  --color-muted: #4b5563;
  --color-surface: #ffffff;
  --color-border: #e5e7eb;
  --color-accent: #2563eb;

  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;

  --radius-md: 8px;
  --radius-full: 999px;

  --font-body: system-ui, -apple-system, "Segoe UI", sans-serif;
  --text-sm: 14px;
  --text-md: 16px;
  --text-xl: 24px;
}
EOF

cat > src/components/Button.tsx <<'EOF'
import './Button.css';

type Props = {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: 'primary' | 'ghost';
  pressed?: boolean;
};

export function Button({ children, onClick, variant = 'primary', pressed }: Props) {
  return (
    <button type="button" className={`button button-${variant}`} aria-pressed={pressed} onClick={onClick}>
      {children}
    </button>
  );
}
EOF

cat > src/components/Button.css <<'EOF'
.button {
  font: 500 var(--text-sm) / 1.4 var(--font-body);
  padding: var(--space-2) var(--space-4);
  border: 1px solid transparent;
  border-radius: var(--radius-md);
  cursor: pointer;
}

.button-primary {
  background: var(--color-accent);
  color: #ffffff;
}

.button-ghost {
  background: transparent;
  color: var(--color-text);
  border-color: var(--color-border);
}

.button:focus-visible {
  outline: 2px solid var(--color-text);
  outline-offset: 2px;
}
EOF

cat > src/components/Toolbar.tsx <<'EOF'
import { Button } from './Button';
import './Toolbar.css';

type Props = {
  filters: string[];
  active: string;
  onSelect: (filter: string) => void;
  onRefresh: () => void;
};

export function Toolbar({ filters, active, onSelect, onRefresh }: Props) {
  return (
    <div className="toolbar">
      {filters.map((filter) => (
        <Button
          key={filter}
          variant={filter === active ? 'primary' : 'ghost'}
          pressed={filter === active}
          onClick={() => onSelect(filter)}
        >
          {filter}
        </Button>
      ))}
      <Button variant="ghost" onClick={onRefresh}>
        Refresh
      </Button>
    </div>
  );
}
EOF

cat > src/components/Toolbar.css <<'EOF'
.toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--color-border);
}
EOF

cat > src/components/CategoryChips.tsx <<'EOF'
import type { Category } from '../api/feed';
import './CategoryChips.css';

type Props = {
  categories: Category[];
  selected: string;
  onSelect: (id: string) => void;
};

export function CategoryChips({ categories, selected, onSelect }: Props) {
  return (
    <ul className="chips" aria-label="Categories">
      {categories.map((category) => (
        <li key={category.id}>
          <button
            type="button"
            className="chip"
            aria-pressed={category.id === selected}
            onClick={() => onSelect(category.id)}
          >
            {category.label}
          </button>
        </li>
      ))}
    </ul>
  );
}
EOF

cat > src/components/CategoryChips.css <<'EOF'
.chips {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin: 0;
  padding: var(--space-3) var(--space-4);
  list-style: none;
}

.chip {
  font: 500 var(--text-sm) / 1.4 var(--font-body);
  padding: var(--space-1) var(--space-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  background: var(--color-surface);
  color: var(--color-text);
  cursor: pointer;
}

.chip[aria-pressed='true'] {
  border-color: var(--color-accent);
  color: var(--color-accent);
}

.chip:focus-visible {
  outline: 2px solid var(--color-text);
  outline-offset: 2px;
}
EOF

cat > src/components/FeedList.tsx <<'EOF'
import type { Article } from '../api/feed';
import './FeedList.css';

export function FeedList({ items }: { items: Article[] }) {
  if (items.length === 0) {
    return <p className="feed-empty">No articles in this category yet.</p>;
  }
  return (
    <ul className="feed">
      {items.map((item) => (
        <li key={item.id} className="feed-item">
          <a className="feed-link" href={`/articles/${item.id}`}>
            {item.title}
          </a>
          <p className="feed-meta">
            {item.source} · <time dateTime={item.publishedAt}>{item.publishedLabel}</time>
          </p>
        </li>
      ))}
    </ul>
  );
}
EOF

cat > src/components/FeedList.css <<'EOF'
.feed {
  margin: 0;
  padding: 0 var(--space-4);
  list-style: none;
}

.feed-item {
  padding: var(--space-3) 0;
  border-bottom: 1px solid var(--color-border);
}

.feed-link {
  font: 600 var(--text-md) / 1.4 var(--font-body);
  color: var(--color-text);
  text-decoration: none;
}

.feed-link:hover {
  text-decoration: underline;
}

.feed-meta,
.feed-empty {
  margin: var(--space-1) 0 0;
  font-size: var(--text-sm);
  line-height: 1.5;
  color: var(--color-muted);
}
EOF

cat > src/api/feed.ts <<'EOF'
export type Category = { id: string; label: string };

export type Article = {
  id: string;
  title: string;
  source: string;
  category: string;
  publishedAt: string;
  publishedLabel: string;
  score: number;
};

async function getJson<T>(path: string): Promise<T> {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`${path} ${res.status}`);
  return res.json() as Promise<T>;
}

export function fetchCategories(): Promise<Category[]> {
  return getJson<Category[]>('/api/categories');
}

export function fetchFeed(category: string): Promise<Article[]> {
  return getJson<Article[]>(`/api/feed?category=${encodeURIComponent(category)}`);
}

export function fetchArticleBody(id: string): Promise<{ id: string; html: string }> {
  return getJson(`/api/articles/${encodeURIComponent(id)}`);
}
EOF

cat > src/pages/Home.tsx <<'EOF'
import { useEffect, useState } from 'react';
import { fetchCategories, fetchFeed, type Article, type Category } from '../api/feed';
import { CategoryChips } from '../components/CategoryChips';
import { FeedList } from '../components/FeedList';
import { Toolbar } from '../components/Toolbar';
import './Home.css';

const FILTERS = ['Latest', 'Top', 'Saved', 'Following'];

export function Home() {
  const [category, setCategory] = useState('all');
  const [filter, setFilter] = useState('Latest');
  const [reloadKey, setReloadKey] = useState(0);
  const [categories, setCategories] = useState<Category[]>([]);
  const [items, setItems] = useState<Article[]>([]);
  const [status, setStatus] = useState<'loading' | 'ready' | 'error'>('loading');

  useEffect(() => {
    let cancelled = false;
    async function load() {
      setStatus('loading');
      try {
        const nextCategories = await fetchCategories();
        const nextItems = await fetchFeed(category);
        if (cancelled) return;
        setCategories(nextCategories);
        setItems(nextItems);
        setStatus('ready');
      } catch {
        if (!cancelled) setStatus('error');
      }
    }
    load();
    return () => {
      cancelled = true;
    };
  }, [category, reloadKey]);

  const visible = items
    .filter((item) => filter !== 'Saved' || item.score > 0)
    .sort((a, b) => (filter === 'Top' ? b.score - a.score : b.publishedAt.localeCompare(a.publishedAt)));

  return (
    <main className="home">
      <h1 className="home-title">Signal feed</h1>
      <Toolbar
        filters={FILTERS}
        active={filter}
        onSelect={setFilter}
        onRefresh={() => setReloadKey((key) => key + 1)}
      />
      <CategoryChips categories={categories} selected={category} onSelect={setCategory} />
      {status === 'loading' && <p role="status">Loading articles…</p>}
      {status === 'error' && (
        <p role="alert">
          Couldn’t load articles. Check your connection, then{' '}
          <button type="button" onClick={() => setReloadKey((key) => key + 1)}>
            try again
          </button>
          .
        </p>
      )}
      {status === 'ready' && <FeedList items={visible} />}
    </main>
  );
}
EOF

cat > src/pages/Home.css <<'EOF'
.home {
  max-width: 720px;
  margin: 0 auto;
  font-family: var(--font-body);
  color: var(--color-text);
  background: var(--color-surface);
}

.home-title {
  margin: 0;
  padding: var(--space-6) var(--space-4) var(--space-2);
  font-size: var(--text-xl);
  line-height: 1.25;
}
EOF

cat > server/categories.ts <<'EOF'
// Canonical category slugs the ingest pipeline stores on articles.
export const CANONICAL = ['ai', 'ai-tools', 'llm', 'design', 'infra', 'product'] as const;

// Source feeds use their own slugs; map them onto canonical ones.
const ALIASES: Record<string, string> = {
  'machine-learning': 'ai',
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

  it('keeps canonical slugs', () => {
    expect(normalizeCategory('llm')).toBe('llm');
    expect(normalizeCategory('ai-tools')).toBe('ai-tools');
  });

  it('sends unknown slugs to other', () => {
    expect(normalizeCategory('gardening')).toBe('other');
  });
});
EOF

cat > server/migrations/0006_add_category_hidden.sql <<'EOF'
ALTER TABLE categories ADD COLUMN hidden BOOLEAN NOT NULL DEFAULT FALSE;
EOF

git add -A
git commit -q -m 'Add signal feed home page and category ingest'
