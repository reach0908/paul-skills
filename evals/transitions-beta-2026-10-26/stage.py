#!/usr/bin/env python3
"""Stage a trial plugin outside the repository for the transitions beta.

candidate: the promoted plugin plus skills/in-progress/transitions.
baseline:  the promoted plugin as on this branch.
The cases are copied to <out>/evals/transitions. The out directory must not exist.
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
arm, out = sys.argv[1], Path(sys.argv[2])
assert arm in ('candidate', 'baseline'), 'arm must be candidate or baseline'
assert not out.exists(), f'{out} exists; choose a fresh directory'
manifest = json.loads((root / '.claude-plugin/plugin.json').read_text())
skills = [s.removeprefix('./') for s in manifest['skills']]
if arm == 'candidate':
    skills.append('skills/in-progress/transitions')
    manifest['skills'] = manifest['skills'] + ['./skills/in-progress/transitions']
(out / '.claude-plugin').mkdir(parents=True)
(out / '.claude-plugin/plugin.json').write_text(json.dumps(manifest, indent=2) + '\n')
for rel in skills:
    shutil.copytree(root / rel, out / rel)
shutil.copytree(Path(__file__).parent / 'cases', out / 'evals/transitions')
files = {p.relative_to(out).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
         for p in sorted(out.rglob('*')) if p.is_file()}
digest = hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()
tree = {p.relative_to(root / 'skills/in-progress/transitions').as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted((root / 'skills/in-progress/transitions').rglob('*')) if p.is_file()}
print(json.dumps({'arm': arm, 'skills': len(skills), 'files': len(files), 'stageDigest': f'sha256:{digest}',
                  'transitionsTree': 'sha256:' + hashlib.sha256(json.dumps(tree, sort_keys=True).encode()).hexdigest()}))
