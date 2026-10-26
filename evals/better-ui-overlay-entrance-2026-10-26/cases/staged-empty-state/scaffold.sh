#!/usr/bin/env bash
# O-N fixture: a vanilla projects page whose first-view empty state (icon, title, description, actions)
# appears all at once with no motion. A staged entrance fits here, so better-ui's recipe should apply.
set -euo pipefail
mkdir -p src

cat > package.json <<'EOF'
{ "name": "projects", "private": true, "version": "1.0.0", "scripts": { "start": "npx serve ." } }
EOF

cat > index.html <<'EOF'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Projects</title>
  <link rel="stylesheet" href="src/styles.css">
</head>
<body>
  <header class="topbar">
    <span class="brand">Ledger</span>
  </header>

  <main class="projects">
    <section class="empty-state" aria-labelledby="empty-title">
      <svg class="empty-icon" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
        <path d="M3 7h6l2 2h10v10H3z"/>
      </svg>
      <h1 id="empty-title">No projects yet</h1>
      <p>Projects group your ledgers, exports and teammates. Create one to get started.</p>
      <div class="actions">
        <a class="primary" href="/projects/new">Create project</a>
        <a class="secondary" href="/import">Import from CSV</a>
      </div>
    </section>
  </main>
</body>
</html>
EOF

cat > src/styles.css <<'EOF'
:root {
  --color-text: #1d2939;
  --color-muted: #475467;
  --color-border: #d0d5dd;
  --radius-md: 10px;
}
body { margin: 0; font-family: system-ui, sans-serif; color: var(--color-text); }
.topbar { padding: 12px 24px; border-bottom: 1px solid var(--color-border); }

.projects { display: grid; place-items: center; min-height: 70vh; padding: 24px; }
.empty-state { max-width: 420px; display: grid; justify-items: center; gap: 12px; text-align: center; }
.empty-icon { color: var(--color-muted); }
.empty-state h1 { margin: 0; font-size: 20px; }
.empty-state p { margin: 0; color: var(--color-muted); }
.actions { display: flex; gap: 8px; margin-top: 8px; }
.primary, .secondary { border-radius: var(--radius-md); padding: 10px 14px; text-decoration: none; }
.primary { background: #1d2939; color: #fff; }
.secondary { border: 1px solid var(--color-border); color: inherit; }
EOF
