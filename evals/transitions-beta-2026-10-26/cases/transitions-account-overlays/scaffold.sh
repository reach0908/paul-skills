#!/usr/bin/env bash
# T-01 fixture: a vanilla page whose account dropdown and saved toast toggle the hidden attribute,
# so both pop with no motion, and whose delete modal uses transition: all 400ms with a display flip.
set -euo pipefail
mkdir -p src

cat > package.json <<'EOF'
{ "name": "account-settings", "private": true, "version": "1.0.0", "scripts": { "start": "npx serve ." } }
EOF

cat > index.html <<'EOF'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Account settings</title>
  <link rel="stylesheet" href="src/tokens.css">
  <link rel="stylesheet" href="src/styles.css">
</head>
<body>
  <header class="topbar">
    <span class="brand">Ledger</span>
    <div class="account">
      <button id="account-button" class="account-button" aria-haspopup="menu" aria-expanded="false" aria-controls="account-menu">Mina Park</button>
      <ul id="account-menu" class="menu" role="menu" hidden>
        <li role="none"><a role="menuitem" href="/profile">Profile</a></li>
        <li role="none"><a role="menuitem" href="/billing">Billing</a></li>
        <li role="none"><a role="menuitem" href="/logout">Sign out</a></li>
      </ul>
    </div>
  </header>

  <main class="settings">
    <h1>Settings</h1>
    <label for="display-name">Display name</label>
    <input id="display-name" value="Mina Park">
    <div class="actions">
      <button id="save-button" class="primary">Save changes</button>
      <button id="delete-button" class="danger">Delete account</button>
    </div>
  </main>

  <div id="toast" class="toast" role="status" hidden>Changes saved</div>

  <div id="delete-modal" class="modal" role="dialog" aria-modal="true" aria-labelledby="delete-title">
    <div class="modal-card">
      <h2 id="delete-title">Delete account?</h2>
      <p>This removes your ledger and every export. It cannot be undone.</p>
      <div class="actions">
        <button id="cancel-delete">Cancel</button>
        <button id="confirm-delete" class="danger">Delete</button>
      </div>
    </div>
  </div>

  <script src="src/app.js"></script>
</body>
</html>
EOF

cat > src/tokens.css <<'EOF'
:root {
  --color-surface: #ffffff;
  --color-text: #1d2939;
  --color-border: #d0d5dd;
  --color-danger: #b42318;
  --radius-md: 10px;
  --shadow-overlay: 0 12px 32px rgb(16 24 40 / 0.18);
  --duration-short: 150ms;
  --duration-medium: 250ms;
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
}
EOF

cat > src/styles.css <<'EOF'
body { margin: 0; font-family: system-ui, sans-serif; color: var(--color-text); }
.topbar { display: flex; justify-content: space-between; align-items: center; padding: 12px 24px; border-bottom: 1px solid var(--color-border); }
.account { position: relative; }
.account-button { background: none; border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 8px 12px; }

.menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 180px;
  margin: 0;
  padding: 6px;
  list-style: none;
  background: var(--color-surface);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-overlay);
}
.menu a { display: block; padding: 8px 10px; color: inherit; text-decoration: none; border-radius: 6px; }
.menu a:hover { background: #f2f4f7; }

.settings { max-width: 480px; margin: 32px auto; display: grid; gap: 12px; }
.actions { display: flex; gap: 8px; }
.primary { background: #1d2939; color: #fff; border: 0; border-radius: var(--radius-md); padding: 10px 14px; }
.danger { background: var(--color-danger); color: #fff; border: 0; border-radius: var(--radius-md); padding: 10px 14px; }

.toast {
  position: fixed;
  bottom: 24px;
  left: 50%;
  translate: -50% 0;
  padding: 12px 16px;
  background: #1d2939;
  color: #fff;
  border-radius: var(--radius-md);
}

.modal {
  position: fixed;
  inset: 0;
  display: none;
  align-items: center;
  justify-content: center;
  background: rgb(16 24 40 / 0.5);
  opacity: 0;
  transition: all 400ms ease;
}
.modal.is-open { display: flex; opacity: 1; }
.modal-card { background: var(--color-surface); border-radius: var(--radius-md); padding: 24px; max-width: 400px; box-shadow: var(--shadow-overlay); }
EOF

cat > src/app.js <<'EOF'
const accountButton = document.getElementById('account-button');
const menu = document.getElementById('account-menu');

accountButton.addEventListener('click', () => {
  const open = menu.hidden;
  menu.hidden = !open;
  accountButton.setAttribute('aria-expanded', String(open));
});

document.addEventListener('click', (event) => {
  if (!menu.hidden && !event.target.closest('.account')) {
    menu.hidden = true;
    accountButton.setAttribute('aria-expanded', 'false');
  }
});

const toast = document.getElementById('toast');
let toastTimer;
document.getElementById('save-button').addEventListener('click', () => {
  toast.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { toast.hidden = true; }, 3000);
});

const modal = document.getElementById('delete-modal');
document.getElementById('delete-button').addEventListener('click', () => modal.classList.add('is-open'));
document.getElementById('cancel-delete').addEventListener('click', () => modal.classList.remove('is-open'));
EOF
