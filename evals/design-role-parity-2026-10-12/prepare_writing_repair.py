#!/usr/bin/env python3
"""Prepare current writing inputs with one exposed and one new state task."""
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
    result = base.prepare('better-writing', arm, 3, '-empty-repair')
    run = base.BASE / 'runs' / result['id']
    record = json.loads((run / 'trial.json').read_text())
    shutil.rmtree(run / 'cases/better-writing-01')
    name = 'better-writing-access-empty'
    target = run / 'cases' / name
    shutil.copytree(HERE / 'fixtures/repairs/access-empty', target)
    (target / 'output').mkdir()
    new_case = {'id': name, 'role': 'better-writing', 'task': 'TASK.md',
                'directory': str(target), 'productDirectory': str(target / 'app'),
                'url': f'http://127.0.0.1:48812/runs/{record["id"]}/cases/{name}/app/'}
    old = {case['id']: case for case in record['cases']}
    record['cases'] = [old['better-writing-02'], new_case, old['better-writing-03']]
    record['purpose'] = 'Exposed deletion recovery plus new permission-change task and unchanged brand/undo preservation; repair, not hidden validation.'
    record['inputs'] = {path: digest for path, digest in base.digest_files(run).items()
                        if path != 'trial.json'}
    (run / 'trial.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('arm', choices=['original', 'paul'])
    print(json.dumps(prepare(parser.parse_args().arm)))
