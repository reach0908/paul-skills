#!/usr/bin/env python3
"""Prepare the exposed whole-page task and two new transition controls."""
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


def prepare(arm, suffix='r4-transitions'):
    run_id = f'design-browser-{arm}-{suffix}'
    dest = BASE / 'runs' / run_id
    if dest.exists():
        raise ValueError(f'Refusing to overwrite {dest}')
    sources = [
        ('design-browser-normal-whole-page-anchor', HERE / 'fixtures/planning/design-browser/normal-whole-page-anchor'),
        ('design-browser-new-catalog-scroll', HERE / 'fixtures/supplements/transitions/catalog-scroll'),
        ('design-browser-new-catalog-preloaded', HERE / 'fixtures/supplements/transitions/catalog-preloaded'),
    ]
    cases = []
    for case_id, source in sources:
        target = dest / 'cases' / case_id
        shutil.copytree(source, target)
        (target / 'output').mkdir(exist_ok=True)
        cases.append({'id': case_id, 'directory': str(target), 'productDirectory': str(target),
                      'task': 'TASK.md', 'url': f'http://127.0.0.1:48812/runs/{run_id}/cases/{case_id}/'})
    if arm == 'paul':
        shutil.copytree(skill_directory(ROOT, 'design-browser'), dest / '.agents/skills/design-browser')
    (dest / 'output').mkdir()
    invocation = ('Read .agents/skills/design-browser/SKILL.md and use $design-browser.'
                  if arm == 'paul' else 'Use ordinary capabilities; no design skill supplied.')
    (dest / 'PROMPT.md').write_text(f'''Execute all three local browser tasks in {dest}. {invocation}
Read trial.json and each TASK.md in order. Use only this run inputs, never another run or evaluator rubric. Do not spawn agents. Use installed Playwright CLI with an owned session, read help and snapshots, preserve commands, failures and structured observations. Honor a task-owned server when requested; otherwise supplied URLs are available. Request scoped permission normally when needed. Do not mutate inputs or skills. Each case needs output/report.md in Korean and output/execution.json with case, status, commands, observations, artifacts, failures, unverified, elapsedSeconds and tokens/cost (null when unknown). Report observations, not quality scores. Rough four minutes per case. Close only owned resources.
''')
    inputs = {str(p.relative_to(dest)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(dest.rglob('*')) if p.is_file()}
    (dest / 'trial.json').write_text(json.dumps({
        'id': run_id, 'role': 'design-browser', 'arm': arm, 'repeat': 4, 'kind': 'repair',
        'sourceRevision': None, 'model': 'inherited, no override', 'effort': 'inherited, no override',
        'context': 'fresh context; three cases share context', 'cases': cases, 'inputs': inputs,
        'status': 'prepared'}, indent=2) + '\n')
    return {'id': run_id, 'directory': str(dest), 'prompt': str(dest / 'PROMPT.md')}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('arm', choices=['control', 'paul'])
    parser.add_argument('--suffix', default='r4-transitions')
    args = parser.parse_args()
    print(json.dumps(prepare(args.arm, args.suffix)))
