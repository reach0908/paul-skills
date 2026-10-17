import { TopicCard } from '../library/TopicCard';
import type { Topic } from '../types';

// Route: /collections/:id
export function CollectionPage({ title, related }: { title: string; related: Topic[] }) {
  return (
    <main>
      <h1>{title}</h1>
      <p>Your reading list.</p>
      <footer aria-labelledby="related-heading">
        <h2 id="related-heading">Related topics</h2>
        {related.map((t) => (
          <TopicCard key={t.id} topic={t} />
        ))}
      </footer>
    </main>
  );
}
