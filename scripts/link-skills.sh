#!/usr/bin/env bash
set -euo pipefail

# Maintainer-only symlinks. Existing files and foreign links are never replaced.
# Use an isolated HOME to test before touching a daily workspace.

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DESTS=("$HOME/.claude/skills" "$HOME/.agents/skills")

# Collect the repo's skills once, link into every destination. `deprecated/`
# is retired, and `misc/` is kept around but rarely used and not promoted (see
# each bucket's own README): neither belongs in a daily-driver skill
# directory, so both are skipped here, same as everywhere else non-promoted
# skills are kept out. `in-progress/` IS still linked: it's public on purpose,
# feedback wanted, and this local install is exactly where that feedback loop
# runs.
names=()
srcs=()
while IFS= read -r -d '' skill_md; do
  src="$(dirname "$skill_md")"
  names+=("$(basename "$src")")
  srcs+=("$src")
done < <(find "$REPO/skills" -name SKILL.md -not -path '*/node_modules/*' -not -path '*/deprecated/*' -not -path '*/misc/*' -print0)

# Check every destination before creating any link.
for DEST in "${DESTS[@]}"; do
  if [ -L "$DEST" ]; then
    echo "error: destination is a symlink: $DEST" >&2
    exit 1
  fi
  for i in "${!names[@]}"; do
    target="$DEST/${names[$i]}"
    if [ -e "$target" ] || [ -L "$target" ]; then
      if [ ! -L "$target" ] || [ "$(readlink "$target")" != "${srcs[$i]}" ]; then
        echo "error: existing install would be replaced: $target" >&2
        exit 1
      fi
    fi
  done
done
for DEST in "${DESTS[@]}"; do
  mkdir -p "$DEST"
  for i in "${!names[@]}"; do
    target="$DEST/${names[$i]}"
    if [ ! -L "$target" ]; then
      ln -s "${srcs[$i]}" "$target"
    fi
    echo "linked ${names[$i]} -> ${srcs[$i]} ($DEST)"
  done
done
