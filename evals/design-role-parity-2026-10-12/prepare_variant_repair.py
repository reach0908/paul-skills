#!/usr/bin/env python3
"""Create paired fixed-control repair trials with a new top-toolbar task."""
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
    result = base.prepare('variant', arm, 3, '-focus-repair')
    run = base.BASE / 'runs' / result['id']
    record = json.loads((run / 'trial.json').read_text())
    shutil.rmtree(run / 'cases/variant-select-and-clean')
    name = 'variant-fixed-toolbar'
    target = run / 'cases' / name
    shutil.copytree(HERE / 'fixtures/repairs/fixed-toolbar', target)
    (target / 'output').mkdir()
    fixture_spec = importlib.util.spec_from_file_location('fixture_prepare', HERE / 'fixtures/explicit/prepare.py')
    fixture = importlib.util.module_from_spec(fixture_spec)
    fixture_spec.loader.exec_module(fixture)
    app = target / 'app'
    fixture.git(app, 'init', '--quiet', '-b', 'main')
    fixture.git(app, 'add', '--all')
    fixture.git(app, 'commit', '--quiet', '-m', 'Initial fixed booking toolbar')
    record['cases'] = [case for case in record['cases'] if case['id'] != 'variant-select-and-clean']
    record['cases'].append({'id': name, 'role': 'variant', 'task': 'TASK.md',
                            'directory': str(target), 'productDirectory': str(target / 'app'),
                            'url': f'http://127.0.0.1:48812/runs/{record["id"]}/cases/{name}/app/'})
    record['purpose'] = 'Exposed fixed-footer failure plus new top-toolbar density task; repair evaluation, not hidden validation.'
    record['inputs'] = {path: digest for path, digest in base.digest_files(run).items()
                        if path != 'trial.json'}
    (run / 'trial.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    return {'id': record['id'], 'directory': str(run)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('arm', choices=['original', 'paul'])
    print(json.dumps(prepare(parser.parse_args().arm)))
