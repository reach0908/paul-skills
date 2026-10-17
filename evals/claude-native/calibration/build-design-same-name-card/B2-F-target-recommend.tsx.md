import { TopicCard } from '../components/TopicCard';
import type { Topic } from '../types';

// Route: /collections/:id
export function CollectionPage({ title, related, onFollow }: { title: string; related: Topic[]; onFollow: (id: string) => void }) {
  return (
    <main>
      <h1>{title}</h1>
      <p>Your reading list.</p>
      <footer aria-labelledby="related-heading">
        <h2 id="related-heading">Related topics</h2>
        {related.map((t) => (
          <TopicCard key={t.id} topic={t} onFollow={onFollow} />
        ))}
      </footer>
    </main>
  );
}
