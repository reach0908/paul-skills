#!/usr/bin/env python3
"""Prepare the exposed in-page navigation repair and a new wireframe task."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from skill_paths import skill_directory
BASE = ROOT / '.scratch/design-role-parity-20261012'


def prepare(arm, suffix='r3-navigation'):
    run_id = f'wireframe-{arm}-{suffix}'
    dest = BASE / 'runs' / run_id
    if dest.exists():
        raise ValueError(f'Refusing to overwrite {dest}')
    sources = [(f'wireframe-navigation-{name}', HERE / 'fixtures/supplements/wire-navigation' / name)
               for name in ('seed-skip', 'station-section')]
    cases = []
    for case_id, source in sources:
        target = dest / 'cases' / case_id
        shutil.copytree(source, target)
        (target / 'output').mkdir(exist_ok=True)
        cases.append({'id': case_id, 'directory': str(target), 'productDirectory': str(target),
                      'task': 'TASK.md', 'url': f'http://127.0.0.1:48812/runs/{run_id}/cases/{case_id}/design/'})
    if arm == 'paul':
        for role in ('wireframe', 'design-browser'):
            shutil.copytree(skill_directory(ROOT, role), dest / '.agents/skills' / role)
    (dest / 'output').mkdir()
    invocation = ('Read .agents/skills/wireframe/SKILL.md and its bundled browser dependency; use $wireframe.'
                  if arm == 'paul' else 'Use ordinary capabilities; no design skill supplied.')
    (dest / 'PROMPT.md').write_text(f'''Execute both local wireframe tasks in {dest}. {invocation}
Read trial.json and each TASK.md in order. Use only this run inputs, never another run or evaluator rubric. Do not spawn agents. Use installed Playwright CLI with an owned session, read help and snapshots, preserve commands, failures and structured observations. Honor a task-owned server when requested; otherwise supplied URLs are available. Request scoped permission normally when needed. Change only task-authorized product files and output evidence; keep supplied skills unchanged. Each case needs output/report.md in Korean and output/execution.json with case, status, commands, observations, artifacts, failures, unverified, elapsedSeconds and tokens/cost (null when unknown). Report observations, not quality scores. Rough four minutes per case. Close only owned resources.
''')
    inputs = {str(p.relative_to(dest)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(dest.rglob('*')) if p.is_file()}
    (dest / 'trial.json').write_text(json.dumps({
        'id': run_id, 'role': 'wireframe', 'arm': arm, 'repeat': 3, 'kind': 'repair',
        'sourceRevision': None, 'model': 'inherited, no override', 'effort': 'inherited, no override',
        'context': 'fresh context; two cases share context', 'cases': cases, 'inputs': inputs,
        'status': 'prepared'}, indent=2) + '\n')
    return {'id': run_id, 'directory': str(dest), 'prompt': str(dest / 'PROMPT.md')}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('arm', choices=['control', 'paul'])
    parser.add_argument('--suffix', default='r3-navigation')
    args = parser.parse_args()
    print(json.dumps(prepare(args.arm, args.suffix)))
