#!/usr/bin/env bash
# T-N fixture: transitions already exist on every surface; the request is to retune their values.
set -euo pipefail
mkdir -p src
cat > package.json <<'EOF'
{ "name": "account-settings", "private": true, "version": "1.0.0" }
EOF
cat > src/styles.css <<'EOF'
.menu { opacity: 0; scale: 0.97; transform-origin: top right; transition: opacity 320ms ease-in-out, scale 320ms ease-in-out; }
.menu[data-open] { opacity: 1; scale: 1; }

.toast { opacity: 0; translate: -50% 12px; transition: opacity 500ms linear, translate 500ms linear; }
.toast[data-open] { opacity: 1; translate: -50% 0; }

.modal { opacity: 0; transition: opacity 280ms ease; }
.modal[data-open] { opacity: 1; }
.modal-card { scale: 0.96; transition: scale 450ms cubic-bezier(0.4, 0, 0.2, 1); }
.modal[data-open] .modal-card { scale: 1; }

.button:active { scale: 0.92; transition: scale 200ms ease; }
EOF
