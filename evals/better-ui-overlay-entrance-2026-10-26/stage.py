#!/usr/bin/env python3
"""Stage the promoted plugin outside the repository for the better-ui overlay trial.

before: every promoted skill as at the base commit (origin/main when the fix branched).
after:  every promoted skill as in this working tree.
--better-ui <dir> replaces skills/design/better-ui in either arm (diagnostic ablations).
The cases are copied to <out>/evals/overlay. The out directory must not exist.

usage: stage.py <before|after> <out> [--better-ui <dir>]
"""
import hashlib
import io
import json
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

BASE = 'e5438096106564ded2ddaede61d8061f9f7b9380'
root = Path(__file__).resolve().parents[2]
arm, out = sys.argv[1], Path(sys.argv[2])
override = Path(sys.argv[4]) if len(sys.argv) == 5 and sys.argv[3] == '--better-ui' else None
assert arm in ('before', 'after'), 'arm must be before or after'
assert not out.exists(), f'{out} exists; choose a fresh directory'
if arm == 'before':
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
if override:
    shutil.rmtree(out / 'skills/design/better-ui')
    shutil.copytree(override, out / 'skills/design/better-ui')
if arm == 'before':
    shutil.rmtree(src)
shutil.copytree(Path(__file__).parent / 'cases', out / 'evals/overlay')


def tree_digest(base):
    files = {p.relative_to(base).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in sorted(base.rglob('*')) if p.is_file()}
    return 'sha256:' + hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()


print(json.dumps({'arm': arm, 'override': str(override) if override else None, 'skills': len(skills),
                  'stageDigest': tree_digest(out), 'betterUiTree': tree_digest(out / 'skills/design/better-ui')}))
