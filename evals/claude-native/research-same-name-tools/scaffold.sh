#!/usr/bin/env bash
# R-02 fixture: two fictional hosts ship a tool with the same name and different features.
set -euo pipefail
mkdir -p sources outputs

cat > sources/H1-orbit-skill-forge.md <<'EOF'
# Orbit Agents: skill-forge plugin

Publisher: Orbit Agents. Applies to the `skill-forge` plugin 2.x for Orbit Agents.

## Evaluate

`skill-forge eval` runs a skill against saved cases, compares two skill versions side by side and reports a benchmark table.
EOF

cat > sources/H2-quill-skill-forge.md <<'EOF'
# Quill CLI: built-in skill-forge

Publisher: Quill CLI. Applies to Quill CLI 0.9 and later.

## What it does

The built-in `skill-forge` system skill scaffolds a new skill folder and validates its frontmatter. It has no evaluation or benchmark commands.
EOF

cat > sources/H3-forum-post.md <<'EOF'
# Forum: "skill-forge evals are great"

Author: a forum user. No host or version is named.

I run skill-forge eval on every change and it catches regressions.
EOF
