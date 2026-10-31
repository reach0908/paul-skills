#!/usr/bin/env python3
"""Stage the promoted plugin outside the repository for the interface-review scope trial.

main:   every promoted skill as at BASE (origin/main when this branch started).
branch: every promoted skill as in this working tree.
The cases are copied to <out>/evals/irscope. The out directory must not exist.

usage: stage.py <main|branch> <out>
Digests hash sorted relative paths and SHA-256 contents, without file modes, so they are not
comparable with skill-sources.json's localDigest.
"""
import hashlib
import io
import json
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

BASE = '794b5721e9c923c63df6ba9781a2750caf4823ef'
root = Path(__file__).resolve().parents[2]
arm, out = sys.argv[1], Path(sys.argv[2])
assert arm in ('main', 'branch'), arm
assert not out.exists(), f'{out} exists; choose a fresh directory'
if arm == 'main':
    src = out.with_name(out.name + '.base')
    tar = subprocess.run(['git', '-C', str(root), 'archive', BASE], check=True, capture_output=True).stdout
    tarfile.open(fileobj=io.BytesIO(tar)).extractall(src)
else:
    src = root
manifest = json.loads((src / '.claude-plugin/plugin.json').read_text())
skills = [s.removeprefix('./') for s in manifest['skills']]
(out / '.claude-plugin').mkdir(parents=True)
(out / '.claude-plugin/plugin.json').write_text(json.dumps(manifest, indent=2) + '\n')
for rel in skills:
    shutil.copytree(src / rel, out / rel)
if arm == 'main':
    shutil.rmtree(src)
shutil.copytree(Path(__file__).parent / 'cases', out / 'evals/irscope')


def tree_digest(base):
    files = {p.relative_to(base).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in sorted(base.rglob('*')) if p.is_file()}
    return 'sha256:' + hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()


design = out / 'skills/design'
print(json.dumps({'arm': arm, 'skills': len(skills), 'stageDigest': tree_digest(out),
                  'interfaceReviewTree': tree_digest(design / 'interface-review'),
                  'betterInterfaceTree': tree_digest(design / 'better-interface'),
                  'casesTree': tree_digest(out / 'evals/irscope')}))
