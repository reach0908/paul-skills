#!/usr/bin/env python3
"""Verify recorded artifact bytes and evaluated skill trees, not AI quality."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

here = Path(__file__).resolve().parent
repo = here.parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--artifact-root', type=Path, default=here)
args = parser.parse_args()
manifest = json.loads((here / 'integrity.json').read_text())
for rel, expected in manifest['artifacts'].items():
    path = args.artifact_root / rel
    if not path.resolve().is_relative_to(args.artifact_root.resolve()) or path.is_symlink():
        raise SystemExit('Unsafe artifact path: ' + rel)
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit('Artifact digest mismatch: ' + rel)
spec = importlib.util.spec_from_file_location('compare', repo / 'skills/in-progress/upstream-sync/scripts/compare.py')
compare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compare)
for path, expected in manifest['skillTrees'].items():
    if compare.digest(compare.local_tree(repo, path)) != expected:
        raise SystemExit('Skill tree digest mismatch: ' + path)
print(str(len(manifest['artifacts'])) + ' artifacts and ' + str(len(manifest['skillTrees'])) + ' skill trees verified; no behavior verdict inferred')
