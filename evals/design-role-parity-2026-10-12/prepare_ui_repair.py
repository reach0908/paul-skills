#!/usr/bin/env python3
"""Freeze an exposed geometry review, a new choice review and a motion regression task."""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent


def prepare(arm):
    spec = importlib.util.spec_from_file_location('role_prepare', HERE / 'prepare.py')
    base = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(base)
    result = base.prepare('better-ui', arm, 3, '-geometry-repair')
    run = base.BASE / 'runs' / result['id']
    record = json.loads((run / 'trial.json').read_text())
    shutil.rmtree(run / 'cases/better-ui-01')
    name = 'better-ui-choice-geometry'
    target = run / 'cases' / name
    shutil.copytree(HERE / 'fixtures/repairs/choice-geometry', target)
    (target / 'output').mkdir()
    new_case = {'id': name, 'role': 'better-ui', 'task': 'TASK.md',
                'directory': str(target), 'productDirectory': str(target / 'app'),
                'url': f'http://127.0.0.1:48812/runs/{record["id"]}/cases/{name}/app/'}
    old = {case['id']: case for case in record['cases']}
    record['cases'] = [old['better-ui-03'], new_case, old['better-ui-02']]
    record['purpose'] = 'Exposed filter shift, new independent choices with reserved-border control, and preserved motion repair. Not hidden validation.'
    record['inputs'] = {path: digest for path, digest in base.digest_files(run).items()
                        if path != 'trial.json'}
    (run / 'trial.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('arm', choices=['original', 'paul'])
    print(json.dumps(prepare(parser.parse_args().arm)))
