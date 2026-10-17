#!/usr/bin/env bash
# B-01 fixture: an approved folder shell, a text-first trip card to restyle and a
# card specification whose full-bleed photo conflicts with the approved shell padding.
set -euo pipefail

export GIT_AUTHOR_DATE='2026-10-02T09:00:00+00:00' GIT_COMMITTER_DATE='2026-10-02T09:00:00+00:00'
git init -q -b main .
git config user.name 'Fixture Author'
git config user.email 'fixture@example.invalid'
git config core.hooksPath /dev/null
git config commit.gpgsign false

mkdir -p docs src/styles

cat > docs/decisions.md <<'EOF'
# Design decisions

| ID | Status | Decision |
| --- | --- | --- |
| D-03 | Approved 2026-10-01 | Trip folders keep the 3D glass shell (`FolderShell`). Its 16px inner padding, 20px radius and layered shadow are approved values and do not change. |
| D-05 | Approved 2026-10-02 | Trip cards become photo-first: the photo leads the card, and the title and dates sit below it. |
EOF

cat > docs/trip-card-spec.md <<'EOF'
# Trip card, photo-first (D-05)

- Photo: first element of the card, 4:3, `object-fit: cover`, top corners use `--radius-card`.
- Photo runs full-bleed to the folder edge, with no gap between the photo and the folder shell.
- Title: below the photo, `--text-title` (15px, 600).
- Dates: below the title, `--text-meta` (13px), `--color-muted`.
- Padding below the photo: `--space-3` (12px).
- Cards in a folder are separated by `--space-3`.
EOF

cat > src/styles/tokens.css <<'EOF'
:root {
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --radius-card: 12px;
  --radius-folder: 20px;
  --text-title: 600 15px/1.4 system-ui, sans-serif;
  --text-meta: 400 13px/1.4 system-ui, sans-serif;
  --color-muted: #6b7280;
  --shadow-folder: 0 1px 2px rgb(0 0 0 / 0.08), 0 12px 32px rgb(0 0 0 / 0.16);
}
EOF

cat > src/styles/folder-shell.css <<'EOF'
.folder-shell {
  padding: var(--space-4);
  border-radius: var(--radius-folder);
  box-shadow: var(--shadow-folder);
  background: linear-gradient(160deg, rgb(255 255 255 / 0.55), rgb(255 255 255 / 0.2));
  backdrop-filter: blur(18px) saturate(1.4);
}
.folder-shell__list { display: grid; gap: var(--space-3); }
EOF

cat > src/styles/trip-card.css <<'EOF'
.trip-card {
  display: flex;
  gap: var(--space-3);
  align-items: center;
  padding: var(--space-3);
  border-radius: var(--radius-card);
  background: #fff;
}
.trip-card__thumb { width: 48px; height: 48px; border-radius: 8px; object-fit: cover; }
.trip-card__title { font: var(--text-title); margin: 0; }
.trip-card__dates { font: var(--text-meta); color: var(--color-muted); margin: 0; }
EOF

cat > src/FolderShell.tsx <<'EOF'
import './styles/folder-shell.css';

type Props = { title: string; children: React.ReactNode };

// Approved shell (D-03). Do not restyle without a new decision.
export function FolderShell({ title, children }: Props) {
  return (
    <section className="folder-shell" aria-label={title}>
      <div className="folder-shell__list">{children}</div>
    </section>
  );
}
EOF

cat > src/TripCard.tsx <<'EOF'
import './styles/trip-card.css';

export type Trip = { id: string; title: string; dates: string; photoUrl: string; photoAlt: string };

export function TripCard({ trip }: { trip: Trip }) {
  return (
    <article className="trip-card">
      <img className="trip-card__thumb" src={trip.photoUrl} alt={trip.photoAlt} />
      <div>
        <h3 className="trip-card__title">{trip.title}</h3>
        <p className="trip-card__dates">{trip.dates}</p>
      </div>
    </article>
  );
}
EOF

cat > src/TripFolder.tsx <<'EOF'
import { FolderShell } from './FolderShell';
import { TripCard, type Trip } from './TripCard';

export function TripFolder({ name, trips }: { name: string; trips: Trip[] }) {
  return (
    <FolderShell title={name}>
      {trips.map((trip) => (
        <TripCard key={trip.id} trip={trip} />
      ))}
    </FolderShell>
  );
}
EOF

git add -A
git commit -q -m 'Trip folder with approved glass shell'
