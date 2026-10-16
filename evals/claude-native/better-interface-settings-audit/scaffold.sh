#!/usr/bin/env bash
# A-01 fixture: a settings screen with an unnamed icon-only delete button and a vague error.
set -euo pipefail

export GIT_AUTHOR_DATE='2026-10-04T09:00:00+00:00' GIT_COMMITTER_DATE='2026-10-04T09:00:00+00:00'
git init -q -b main .
git config user.name 'Fixture Author'
git config user.email 'fixture@example.invalid'
git config core.hooksPath /dev/null
git config commit.gpgsign false

mkdir -p src

cat > src/icons.tsx <<'EOF'
export function TrashIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5">
      <path d="M4 6h12M8 6V4h4v2M6 6l1 10h6l1-10" />
    </svg>
  );
}
EOF

cat > src/Settings.tsx <<'EOF'
import { TrashIcon } from './icons';
import './settings.css';

type Props = { email: string; onDeleteAccount: () => void; error?: string };

export function Settings({ email, onDeleteAccount, error }: Props) {
  return (
    <main className="settings">
      <h1>Settings</h1>
      <section className="settings__account" aria-labelledby="account-heading">
        <h2 id="account-heading">Account</h2>
        <p className="settings__email">{email}</p>
        <button type="button" className="icon-button" onClick={onDeleteAccount}>
          <TrashIcon />
        </button>
      </section>
      {error && <p className="settings__error">Error occurred.</p>}
    </main>
  );
}
EOF

cat > src/settings.css <<'EOF'
.settings { max-width: 40rem; margin: 0 auto; padding: 1.5rem 1rem; }
.settings__account { display: flex; align-items: center; gap: 0.75rem; }
.settings__email { flex: 1; min-width: 0; overflow-wrap: anywhere; }
.icon-button { inline-size: 2.75rem; block-size: 2.75rem; display: grid; place-items: center; }
.settings__error { color: #b42318; }
EOF

git add -A
git commit -q -m 'Settings screen'
