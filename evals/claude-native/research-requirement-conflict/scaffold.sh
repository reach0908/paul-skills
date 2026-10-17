#!/usr/bin/env bash
# R-03 fixture: the user's two goals cannot both be met with the named framework feature.
set -euo pipefail
mkdir -p sources outputs

cat > sources/K1-glasskit-glass-effect.md <<'EOF'
# GlassKit 4: glassEffect

Publisher: GlassKit team. Applies to GlassKit 4.

## Overview

`glassEffect()` renders a translucent glass material inside a view's 2D shape, refracting the content behind the view. It is designed for controls, toolbars and cards.

## Limits

`glassEffect()` does not render volumetric or 3D geometry. Inside a 3D scene, use a transparent physically based material instead.
EOF

cat > sources/K2-depthkit-materials.md <<'EOF'
# DepthKit 2: physically based materials

Publisher: DepthKit team. Applies to DepthKit 2.

## Transparent materials

`TransparentMaterial` renders refraction and thickness on 3D meshes. Particle systems such as sand can render inside a transparent mesh in the same scene.
EOF
