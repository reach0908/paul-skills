#!/usr/bin/env bash
# R-01 fixture: four supplied sources for a fictional product. Runs in the empty
# eval workspace. Keep it self-contained; the runner may not expose sibling files.
set -euo pipefail

mkdir -p sources outputs

cat > sources/D1-atlas-import-v2-manual.md <<'EOF'
# Atlas Import v2 manual

Publisher: Atlas Import product team. Applies to version 2.

## Getting started

Install the importer and sign in with your workspace account.

## Import

CSV files up to 20 MB are supported. XLSX is not supported.
EOF

cat > sources/D2-atlas-import-v1-manual.md <<'EOF'
# Atlas Import v1 manual

Publisher: Atlas Import product team. Applies to version 1.

## Import

CSV files up to 5 MB are supported.
EOF

cat > sources/D3-third-party-blog.md <<'EOF'
# Five things I learned about Atlas Import

Author: an independent blogger. No product version or test method is given.

Atlas Import uploads are limited to 5 MB.
EOF

cat > sources/D4-atlas-import-v2-release-notes.md <<'EOF'
# Atlas Import v2 release notes

Publisher: Atlas Import product team.

## Limits

The CSV limit increased from 5 MB to 20 MB.
EOF
