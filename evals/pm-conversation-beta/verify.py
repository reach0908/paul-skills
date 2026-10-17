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
ledger = json.loads((here / 'public-copy.json').read_text())
original_bytes = (here / ledger['original_manifest']).read_bytes()
if hashlib.sha256(original_bytes).hexdigest() != ledger['original_manifest_sha256']:
    raise SystemExit('Original manifest digest mismatch')
original = json.loads(original_bytes)
if original['artifacts'].keys() != manifest['artifacts'].keys() or original['skillTrees'] != manifest['skillTrees']:
    raise SystemExit('Public copy changed evidence membership or skill trees')
redacted = {row['path']: row for row in ledger['files']}
if len(redacted) != len(ledger['files']):
    raise SystemExit('Duplicate public-copy record')
amended = {row['path']: row for row in ledger['maintenance']}
if len(amended) != len(ledger['maintenance']) or redacted.keys() & amended.keys():
    raise SystemExit('Duplicate maintenance record')
for row in redacted.values():
    if row['replacement_count'] < 1:
        raise SystemExit('Invalid redaction count')
changes = dict(redacted, **amended)
for rel, row in changes.items():
    if (row['original_sha256'] != original['artifacts'].get(rel)
            or row['public_sha256'] != manifest['artifacts'].get(rel)):
        raise SystemExit('Public-copy ledger mismatch: ' + rel)
for rel, expected in original['artifacts'].items():
    if rel not in changes and manifest['artifacts'][rel] != expected:
        raise SystemExit('Unrecorded public-copy change: ' + rel)
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
print(str(len(manifest['artifacts'])) + ' public artifacts, ' + str(len(redacted)) +
      ' recorded redactions, ' + str(len(amended)) + ' maintenance amendments and ' + str(len(manifest['skillTrees'])) +
      ' skill trees verified; no behavior verdict inferred')
