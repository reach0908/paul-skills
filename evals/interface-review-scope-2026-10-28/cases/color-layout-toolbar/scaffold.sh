#!/usr/bin/env bash
# S-03: a real UI change. The accent token is lightened (white button text drops from 5.17:1
# to 2.54:1; accent-colored chip text on white is 2.54:1 too) and the toolbar moves from a
# wrapping flex row to a fixed five-column grid (880px wide, overflowing a 320px viewport)
# with a raw 12px gap in place of the spacing token. Markup and strings are unchanged.
set -euo pipefail
source "$(dirname "$0")/../base.sh"

git switch -q -c design/accent-toolbar
export GIT_AUTHOR_DATE='2026-10-21T09:00:00+00:00' GIT_COMMITTER_DATE='2026-10-21T09:00:00+00:00'

sed -i.bak 's/--color-accent: #2563eb;/--color-accent: #60a5fa;/' src/styles/tokens.css
rm src/styles/tokens.css.bak

cat > src/components/Toolbar.css <<'EOF'
.toolbar {
  display: grid;
  grid-template-columns: repeat(5, 160px);
  gap: 12px;
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--color-border);
}
EOF

git add -A
git commit -q -m 'Refresh accent color and align toolbar buttons' -m 'Lighter accent to match the new brand sheet; toolbar buttons now sit on an even grid.'
