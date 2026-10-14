#!/usr/bin/env python3
"""Prepare isolated skill arms. Does not call a model, browser, or network."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from skill_paths import skill_directory


def file_hash(data):
    return hashlib.sha256(data).hexdigest()


def prepare(destination, arm, upstream=None):
    destination = Path(destination).absolute()
    if destination.exists() or destination.is_symlink():
        raise ValueError('Use a new destination for every trial')
    manifest = json.loads((HERE / 'upstream-manifest.json').read_text())
    names = sorted({PurePosixPath(p).parts[1] for p in manifest['files'] if p.endswith('/SKILL.md')})
    files = {}
    if arm == 'upstream':
        if upstream is None:
            raise ValueError('--upstream is required for the upstream arm')
        revision = manifest['revision']
        for path, expected in manifest['files'].items():
            data = subprocess.check_output(['git', '-C', str(upstream), 'show', f'{revision}:{path}'])
            if file_hash(data) != expected:
                raise ValueError(f'Upstream content mismatch: {path}')
            files[path] = data
        notice = files.pop('LICENSE')
        for name in names:
            files[f'skills/{name}/LICENSE'] = notice
    elif arm == 'paul':
        for name in [*names, 'design-browser']:
            folder = skill_directory(ROOT, name)
            if folder.is_symlink() or not (folder / 'SKILL.md').is_file():
                raise ValueError(f'Missing or linked candidate: {folder}')
            for path in sorted(folder.rglob('*')):
                if path.is_symlink():
                    raise ValueError(f'Symlink in candidate: {path}')
                if path.is_file():
                    files[f'skills/{name}/{path.relative_to(folder).as_posix()}'] = path.read_bytes()
    elif arm != 'no-skill':
        raise ValueError('Unknown arm')
    for path in files:
        parsed = PurePosixPath(path)
        if parsed.is_absolute() or '..' in parsed.parts or parsed.parts[0] != 'skills':
            raise ValueError(f'Invalid bundle path: {path}')
    task = (HERE / 'cases/inflfeed.md').read_bytes()
    # Validate all sources before creating the candidate's workspace.
    destination.mkdir(parents=True)
    try:
        (destination / 'task.md').write_bytes(task)
        (destination / 'output').mkdir()
        for path, data in files.items():
            relative = PurePosixPath(path).relative_to('skills')
            target = destination / '.agents/skills' / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        hashes = {p: file_hash(data) for p, data in sorted(files.items())}
        record = {
            'protocol': 'design-beta-v1', 'arm': arm,
            'upstreamRevision': manifest['revision'] if arm == 'upstream' else None,
            'taskDigest': file_hash(task), 'skillFiles': hashes,
            'bundleDigest': file_hash(json.dumps(hashes, sort_keys=True, separators=(',', ':')).encode()),
            'model': None, 'hostVersion': None, 'browserVersion': None,
            'status': 'prepared, not executed',
        }
        (destination / 'trial.json').write_text(json.dumps(record, indent=2) + '\n')
    except Exception:
        shutil.rmtree(destination)
        raise
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--arm', choices=['no-skill', 'upstream', 'paul'], required=True)
    parser.add_argument('--upstream', type=Path)
    args = parser.parse_args()
    record = prepare(args.destination, args.arm, args.upstream)
    print(json.dumps({'destination': str(args.destination), 'arm': args.arm,
                      'bundleDigest': record['bundleDigest'], 'status': record['status']}))


if __name__ == '__main__':
    main()
