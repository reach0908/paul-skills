#!/usr/bin/env python3
"""Prepare a fresh visual-variant state-preservation repair pair."""
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
    result = base.prepare('variant', arm, 4, '-state-repair')
    run = base.BASE / 'runs' / result['id']
    record = json.loads((run / 'trial.json').read_text())
    shutil.rmtree(run / 'cases/variant-usage-density')
    name = 'variant-quantity'
    target = run / 'cases' / name
    shutil.copytree(HERE / 'fixtures/repairs/variant-quantity', target)
    (target / 'output').mkdir()
    fixture_spec = importlib.util.spec_from_file_location('fixture_prepare', HERE / 'fixtures/explicit/prepare.py')
    fixture = importlib.util.module_from_spec(fixture_spec)
    fixture_spec.loader.exec_module(fixture)
    app = target / 'app'
    fixture.git(app, 'init', '--quiet', '-b', 'main')
    fixture.git(app, 'add', '--all')
    fixture.git(app, 'commit', '--quiet', '-m', 'Initial local order summary')
    record['cases'] = [case for case in record['cases'] if case['id'] != 'variant-usage-density']
    record['cases'].insert(1, {'id': name, 'role': 'variant', 'task': 'TASK.md',
                             'directory': str(target), 'productDirectory': str(app),
                             'url': f'http://127.0.0.1:48812/runs/{record["id"]}/cases/{name}/app/'})
    record['purpose'] = 'Exposed footer state reset, new independent order-state task, and cleanup preservation. Separate from initial frozen repeats and focus repair.'
    record['inputs'] = {path: digest for path, digest in base.digest_files(run).items()
                        if path != 'trial.json'}
    (run / 'trial.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    return {'id': record['id'], 'directory': str(run)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('arm', choices=['original', 'paul'])
    print(json.dumps(prepare(parser.parse_args().arm)))
