#!/usr/bin/env python3
"""Prepare a new consumer-budget repair trial without overwriting old outputs."""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def prepare(arm, repeat=3):
    base = module('role_prepare', HERE / 'prepare.py')
    fixture = module('fixture_prepare', HERE / 'fixtures/explicit/prepare.py')
    result = base.prepare('interface-review', arm, repeat, '-budget-repair')
    run = base.BASE / 'runs' / result['id']
    record = json.loads((run / 'trial.json').read_text())
    removed = run / 'cases/interface-review-no-change'
    shutil.rmtree(removed)
    name = 'interface-review-consumer-budget'
    target = run / 'cases' / name
    target.mkdir()
    source = HERE / 'fixtures/repairs/consumer-budget'
    shutil.copy2(source / 'TASK.md', target / 'TASK.md')
    shutil.copytree(source / 'app', target / 'app')
    (target / 'output').mkdir()
    app = target / 'app'
    fixture.git(app, 'init', '--quiet', '-b', 'main')
    fixture.git(app, 'add', '--all')
    fixture.git(app, 'commit', '--quiet', '-m', 'Initial shared action fixture')
    sha = fixture.git(app, 'rev-parse', 'HEAD')
    fixture.git(app, 'update-ref', 'refs/remotes/origin/main', sha)
    fixture.git(app, 'symbolic-ref', 'refs/remotes/origin/HEAD', 'refs/remotes/origin/main')
    fixture.git(app, 'switch', '--quiet', '-c', 'codex/local-review')
    css = app / 'components/action.css'
    css.write_text(css.read_text().replace('outline:3px solid #182536; outline-offset:4px;', 'outline:0;'))
    fixture.git(app, 'add', '--all')
    fixture.git(app, 'commit', '--quiet', '-m', 'Simplify shared action focus', timestamp='2026-10-12T00:01:00Z')
    record['cases'] = [case for case in record['cases'] if case['id'] != 'interface-review-no-change']
    record['cases'].append({'id': name, 'role': 'interface-review', 'task': 'TASK.md',
                            'directory': str(target), 'productDirectory': str(app),
                            'url': f'http://127.0.0.1:48812/runs/{record["id"]}/cases/{name}/app/'})
    record['purpose'] = 'Repair exposed budget interpretation and validate on new focus-regression case; not hidden validation.'
    record['inputs'] = {path: digest for path, digest in base.digest_files(run).items()
                        if path != 'trial.json'}
    (run / 'trial.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    return {'id': record['id'], 'directory': str(run)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('arm', choices=['original', 'paul'])
    parser.add_argument('--repeat', type=int, default=3)
    args = parser.parse_args()
    print(json.dumps(prepare(args.arm, args.repeat)))
