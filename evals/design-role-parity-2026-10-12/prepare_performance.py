#!/usr/bin/env python3
"""Freeze a small paired performance-evidence supplement before dispatch."""
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


def prepare(arm):
    run_id = f'design-browser-{arm}-r3-performance'
    dest = BASE / 'runs' / run_id
    if dest.exists():
        raise ValueError(f'Refusing to overwrite {dest}')
    case_id = 'design-browser-performance-local-labels'
    case = dest / 'cases' / case_id
    shutil.copytree(HERE / 'fixtures/supplements/performance', case)
    (case / 'output').mkdir()
    if arm == 'paul':
        shutil.copytree(skill_directory(ROOT, 'design-browser'),
                        dest / '.agents/skills/design-browser')
    invocation = ('Read .agents/skills/design-browser/SKILL.md and use $design-browser.'
                  if arm == 'paul' else 'No design skill is supplied; use ordinary capabilities.')
    (dest / 'PROMPT.md').write_text(f'''Execute the authorized local browser evidence task, not a skill evaluation verdict.
Work only in {dest}. {invocation}
Read trial.json and TASK.md. Use only this task's inputs, never another run, evaluator rubrics or repository skill sources. Do not spawn agents. Use the supplied local server URL. Use installed Playwright CLI with a unique owned session, read help, take a snapshot before selecting controls, preserve commands/errors/returned measurements and close only your session. Request scoped tool permission normally if needed; do not bypass the sandbox.
Create output/report.md in Korean and output/execution.json with case, status, commands, observations, artifacts, failures, unverified, elapsedSeconds, tokens and cost. Unknown telemetry stays null. Save raw structured observations. Keep inputs and skill unchanged. Timebox roughly four minutes; honestly record unavailable observations. Final names report and limits.
''')
    inputs = {str(p.relative_to(dest)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(dest.rglob('*')) if p.is_file()}
    record = {
        'id': run_id, 'role': 'design-browser', 'arm': arm, 'repeat': 3,
        'kind': 'supplement', 'sourceRevision': None,
        'model': 'inherited, no override', 'effort': 'inherited, no override',
        'context': 'fresh independent single-case context',
        'cases': [{'id': case_id, 'directory': str(case),
                   'productDirectory': str(case), 'task': 'TASK.md',
                   'url': f'http://127.0.0.1:48812/runs/{run_id}/cases/{case_id}/'}],
        'inputs': inputs, 'status': 'prepared'}
    (dest / 'trial.json').write_text(json.dumps(record, indent=2) + '\n')
    return {'id': run_id, 'role': 'design-browser', 'arm': arm, 'repeat': 3,
            'directory': str(dest), 'prompt': str(dest / 'PROMPT.md'),
            'kind': 'supplement', 'status': 'prepared'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('arm', choices=['control', 'paul'])
    args = parser.parse_args()
    print(json.dumps(prepare(args.arm)))
