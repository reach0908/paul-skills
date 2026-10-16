.trip-card {
  display: flex;
  gap: var(--space-3);
  align-items: center;
  padding: var(--space-3);
  border-radius: var(--radius-card);
  background: #fff;
}
.trip-card__photo { width: 96px; height: 72px; border-radius: 8px; object-fit: cover; }
.trip-card__body { padding: 0; }
.trip-card__title { font: var(--text-title); margin: 0; }
.trip-card__dates { font: var(--text-meta); color: var(--color-muted); margin: 0; }
