#!/usr/bin/env bash
# S-02: a performance-only change to the home page component. Requests run in parallel, the
# sorted list is memoized and the first three article bodies are prefetched. The JSX the page
# returns, its render conditions and every string and style are unchanged.
set -euo pipefail
source "$(dirname "$0")/../base.sh"

git switch -q -c perf/home-load
export GIT_AUTHOR_DATE='2026-10-21T09:00:00+00:00' GIT_COMMITTER_DATE='2026-10-21T09:00:00+00:00'

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

const bodyCache = new Map<string, Promise<{ id: string; html: string }>>();

export function fetchArticleBody(id: string): Promise<{ id: string; html: string }> {
  let pending = bodyCache.get(id);
  if (!pending) {
    pending = getJson<{ id: string; html: string }>(`/api/articles/${encodeURIComponent(id)}`);
    pending.catch(() => bodyCache.delete(id));
    bodyCache.set(id, pending);
  }
  return pending;
}

export function prefetchArticleBodies(ids: string[]): void {
  for (const id of ids) void fetchArticleBody(id).catch(() => undefined);
}
EOF

cat > src/pages/Home.tsx <<'EOF'
import { useEffect, useMemo, useState } from 'react';
import { fetchCategories, fetchFeed, prefetchArticleBodies, type Article, type Category } from '../api/feed';
import { CategoryChips } from '../components/CategoryChips';
import { FeedList } from '../components/FeedList';
import { Toolbar } from '../components/Toolbar';
import './Home.css';

const FILTERS = ['Latest', 'Top', 'Saved', 'Following'];
const PREFETCH_COUNT = 3;

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
        const [nextCategories, nextItems] = await Promise.all([fetchCategories(), fetchFeed(category)]);
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

  const visible = useMemo(
    () =>
      items
        .filter((item) => filter !== 'Saved' || item.score > 0)
        .sort((a, b) => (filter === 'Top' ? b.score - a.score : b.publishedAt.localeCompare(a.publishedAt))),
    [items, filter],
  );

  useEffect(() => {
    if (status === 'ready') prefetchArticleBodies(visible.slice(0, PREFETCH_COUNT).map((item) => item.id));
  }, [status, visible]);

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

git add -A
git commit -q -m 'Speed up home feed load' -m 'Fetch categories and feed in parallel, memoize the filtered sort and prefetch the first three article bodies. No visual change.'
