#!/usr/bin/env bash
# B-02 fixture: two exported components share the name TopicCard. The reference names a
# route and section, not a file; only the Library page call site identifies the export.
set -euo pipefail

export GIT_AUTHOR_DATE='2026-10-05T09:00:00+00:00' GIT_COMMITTER_DATE='2026-10-05T09:00:00+00:00'
git init -q -b main .
git config user.name 'Fixture Author'
git config user.email 'fixture@example.invalid'
git config core.hooksPath /dev/null
git config commit.gpgsign false

mkdir -p docs src/components src/library src/collection src/styles

cat > docs/reference.md <<'EOF'
# Reference: collection footer

Source: Library page (`/library`), footer section "Explore topics", collapsed state, design revision 2026-10-05.

Reuse the cards from that footer in the "Related topics" footer of the collection detail page (`/collections/:id`). In the Library footer each whole card opens its topic page, including with Enter. Keep that behavior.
EOF

cat > src/types.ts <<'EOF'
export type Topic = { id: string; name: string; count: number };
EOF

cat > src/styles/topic-card.css <<'EOF'
.topic-card { display: grid; gap: 4px; padding: 16px; border-radius: 12px; border: 1px solid #d0d5dd; color: inherit; text-decoration: none; }
.topic-card__faces { font-size: 20px; }
.topic-card__name { font-weight: 600; }
.topic-card__count { color: #667085; }
.topic-card:focus-visible { outline: 3px solid #5327af; outline-offset: 3px; }
EOF

cat > src/components/TopicCard.tsx <<'EOF'
import '../styles/topic-card.css';
import type { Topic } from '../types';

export function TopicCard({ topic, onFollow }: { topic: Topic; onFollow: (id: string) => void }) {
  return (
    <div className="topic-card" onClick={() => onFollow(topic.id)}>
      <span className="topic-card__faces" aria-hidden="true">● ● ●</span>
      <strong className="topic-card__name">{topic.name}</strong>
      <span className="topic-card__count">{topic.count} writers</span>
    </div>
  );
}
EOF

cat > src/library/TopicCard.tsx <<'EOF'
import '../styles/topic-card.css';
import type { Topic } from '../types';

export function TopicCard({ topic }: { topic: Topic }) {
  return (
    <a className="topic-card" href={`/topics/${topic.id}`}>
      <span className="topic-card__faces" aria-hidden="true">● ● ●</span>
      <strong className="topic-card__name">{topic.name}</strong>
      <span className="topic-card__count">{topic.count} writers</span>
    </a>
  );
}
EOF

cat > src/library/LibraryPage.tsx <<'EOF'
import { TopicCard as RecommendedTopic } from '../components/TopicCard';
import { TopicCard } from './TopicCard';
import type { Topic } from '../types';

type Props = { recommended: Topic[]; topics: Topic[]; onFollow: (id: string) => void };

// Route: /library
export function LibraryPage({ recommended, topics, onFollow }: Props) {
  return (
    <main>
      <h1>Library</h1>
      <section aria-labelledby="recommended-heading">
        <h2 id="recommended-heading">Recommended topics</h2>
        {recommended.map((t) => (
          <RecommendedTopic key={t.id} topic={t} onFollow={onFollow} />
        ))}
      </section>
      <footer aria-labelledby="explore-heading">
        <h2 id="explore-heading">Explore topics</h2>
        {topics.map((t) => (
          <TopicCard key={t.id} topic={t} />
        ))}
      </footer>
    </main>
  );
}
EOF

cat > src/collection/CollectionPage.tsx <<'EOF'
import type { Topic } from '../types';

// Route: /collections/:id
export function CollectionPage({ title, related }: { title: string; related: Topic[] }) {
  return (
    <main>
      <h1>{title}</h1>
      <p>Your reading list.</p>
      <footer aria-labelledby="related-heading">
        <h2 id="related-heading">Related topics</h2>
        <ul>
          {related.map((t) => (
            <li key={t.id}>{t.name}</li>
          ))}
        </ul>
      </footer>
    </main>
  );
}
EOF

git add -A
git commit -q -m 'Library and collection pages'
