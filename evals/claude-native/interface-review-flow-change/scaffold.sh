#!/usr/bin/env bash
# I-01 fixture: a staged accessibility regression, an unstaged repair of it, an
# unchanged pre-existing width problem in a staged file and a staged lockfile.
# interface-review-unnamed/scaffold.sh must stay byte-identical to this file.
set -euo pipefail

export GIT_AUTHOR_DATE='2026-10-01T09:00:00+00:00' GIT_COMMITTER_DATE='2026-10-01T09:00:00+00:00'
git init -q -b main .
git config user.name 'Fixture Author'
git config user.email 'fixture@example.invalid'
git config core.hooksPath /dev/null
git config commit.gpgsign false

mkdir -p src

cat > package.json <<'EOF'
{
  "name": "dialog-fixture",
  "private": true,
  "dependencies": {"react": "18.3.1"}
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

cat > src/CloseControl.tsx <<'EOF'
type Props = { onClose: () => void };

export function CloseControl({ onClose }: Props) {
  return (
    <button type="button" className="close-control" aria-label="Close dialog" onClick={onClose}>
      ×
    </button>
  );
}
EOF

cat > src/Dialog.tsx <<'EOF'
import { CloseControl } from './CloseControl';

type Props = { title: string; onClose: () => void; children: React.ReactNode };

export function Dialog({ title, onClose, children }: Props) {
  return (
    <div role="dialog" aria-modal="true" aria-labelledby="dialog-title">
      <h2 id="dialog-title">{title}</h2>
      <CloseControl onClose={onClose} />
      {children}
    </div>
  );
}
EOF

cat > src/LegacyCard.tsx <<'EOF'
export function LegacyCard() {
  return (
    <section className="legacy-card" style={{ width: 480 }}>
      <h3>Legacy plan</h3>
      <p>Your plan renews monthly.</p>
    </section>
  );
}
EOF

git add -A
git commit -q -m 'Add dialog and legacy plan card'

# Staged change: the close control loses its native button semantics.
cat > src/CloseControl.tsx <<'EOF'
type Props = { onClose: () => void };

export function CloseControl({ onClose }: Props) {
  return (
    <div className="close-control" aria-label="Close dialog" onClick={onClose}>
      ×
    </div>
  );
}
EOF

# Staged copy edit next to the unchanged fixed width.
cat > src/LegacyCard.tsx <<'EOF'
export function LegacyCard() {
  return (
    <section className="legacy-card" style={{ width: 480 }}>
      <h3>Legacy plan</h3>
      <p>Your plan renews every month.</p>
    </section>
  );
}
EOF

cat > pnpm-lock.yaml <<'EOF'
lockfileVersion: '9.0'
settings:
  autoInstallPeers: true
importers:
  .:
    dependencies:
      react:
        specifier: 18.3.1
        version: 18.3.1
EOF

git add src/CloseControl.tsx src/LegacyCard.tsx pnpm-lock.yaml

# Unstaged repair: the working tree restores the button, the index does not.
cat > src/CloseControl.tsx <<'EOF'
type Props = { onClose: () => void };

export function CloseControl({ onClose }: Props) {
  return (
    <button type="button" className="close-control" aria-label="Close dialog" onClick={onClose}>
      ×
    </button>
  );
}
EOF
