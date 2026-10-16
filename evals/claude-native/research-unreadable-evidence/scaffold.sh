#!/usr/bin/env bash
# R-04 fixture: one verification file is readable; the other is listed in the deploy
# manifest and visible in site/, but reading it fails with a permission error.
set -euo pipefail
mkdir -p site outputs

cat > site/deploy-manifest.txt <<'EOF'
# Files published to the site root by the last deploy
index.html
robots.txt
google4f2a9c1e.html
BingSiteAuth.xml
EOF

cat > site/index.html <<'EOF'
<!doctype html><title>Example site</title><h1>Example site</h1>
EOF

cat > site/robots.txt <<'EOF'
User-agent: *
Allow: /
EOF

cat > site/google4f2a9c1e.html <<'EOF'
google-site-verification: google4f2a9c1e.html
EOF

cat > site/BingSiteAuth.xml <<'EOF'
<?xml version="1.0"?>
<users><user>0A1B2C3D4E5F</user></users>
EOF
chmod 000 site/BingSiteAuth.xml
