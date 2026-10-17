.trip-card {
  display: flex;
  flex-direction: column;
  border-radius: var(--radius-card);
  background: #fff;
  overflow: hidden;
}
.trip-card__photo {
  inline-size: 100%;
  aspect-ratio: 4 / 3;
  object-fit: cover;
  border-start-start-radius: var(--radius-card);
  border-start-end-radius: var(--radius-card);
}
.trip-card__body { padding: var(--space-3); }
.trip-card__title { font: var(--text-title); margin: 0; }
.trip-card__dates { font: var(--text-meta); color: var(--color-muted); margin: 0; }
