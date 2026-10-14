#!/usr/bin/env python3
"""Prepare a fresh local five-stage exercise outside the maintainer checkout."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from skill_paths import skill_directory


def hashes(folder):
    return {str(p.relative_to(folder)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(folder.rglob('*')) if p.is_file() and '.git' not in p.parts}


def prepare(destination):
    dest = Path(destination).resolve()
    if dest.exists():
        raise ValueError(f'Refusing to overwrite {dest}')
    if subprocess.run(['git', '-C', str(dest.parent), 'rev-parse', '--show-toplevel'],
                      capture_output=True).returncode == 0:
        raise ValueError('Destination must be outside an existing Git checkout')
    shutil.copytree(HERE / 'fixtures/planning/composition', dest)
    subprocess.run(['python3', '-B', 'prepare.py'], cwd=dest, check=True)
    catalog = json.loads((HERE / 'fixtures/planning/composition.json').read_text())
    # Dependencies are copied intact. Each stage reads only its applicable role.
    names = ['information-architecture', 'user-flow', 'wireframe', 'build-design',
             'interface-review', 'better-interface', 'better-accessibility',
             'better-colors', 'better-layout', 'better-typography', 'better-ui',
             'better-writing', 'design-browser']
    for name in names:
        shutil.copytree(skill_directory(ROOT, name),
                        dest / '.agents/skills' / name)
    record = {'id': 'seed-pickup-five-stage', 'status': 'prepared, not executed',
              'directory': str(dest), 'stages': catalog['stages'],
              'inputs': hashes(dest),
              'conditions': 'Fresh context per stage. Actual previous output only. Freeze hashes before and after each stage. Preserve upstream files and failures. No user acceptance inferred.'}
    (dest / 'composition.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({'directory': str(dest), 'status': record['status']}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination')
    prepare(parser.parse_args().destination)
