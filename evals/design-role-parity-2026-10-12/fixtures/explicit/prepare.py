#!/usr/bin/env python3
"""Create a disposable, executor-safe workspace for one explicit-role case."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess

HERE = Path(__file__).resolve().parent


def git(workspace, *args, timestamp='2026-10-12T00:00:00Z'):
    env = dict(os.environ, GIT_AUTHOR_DATE=timestamp, GIT_COMMITTER_DATE=timestamp)
    command = ['git', '-c', 'user.name=Fixture Maintainer', '-c',
               'user.email=fixture@example.invalid', '-c', 'commit.gpgsign=false',
               '-c', 'core.hooksPath=/dev/null', *args]
    result = subprocess.run(command, cwd=workspace, env=env, text=True,
                            capture_output=True, check=True)
    return result.stdout.rstrip('\n')


def copy_tree(source, target):
    for path in sorted(source.rglob('*')):
        relative = path.relative_to(source)
        if path.is_symlink():
            raise ValueError('Fixture symlinks are not supported: ' + str(path))
        if path.is_file():
            output = target / relative
            output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, output)


def prepare(case_id, destination):
    manifest = json.loads((HERE / 'cases.json').read_text())
    case = next((item for item in manifest if item['id'] == case_id), None)
    if not case:
        raise ValueError('Unknown case: ' + case_id)
    source = HERE / case_id
    destination = Path(destination).expanduser().resolve()
    if destination == HERE or HERE in destination.parents:
        raise ValueError('Destination must be outside the immutable fixture tree.')
    if destination.exists() and any(destination.iterdir()):
        raise ValueError('Destination must be new or empty: ' + str(destination))
    destination.mkdir(parents=True, exist_ok=True)
    config_path = source / 'setup' / 'git.json'
    config = json.loads(config_path.read_text()) if config_path.exists() else None
    copy_tree(source / ('setup/base' if config else 'app'), destination)
    git(destination, 'init', '--quiet', '-b', 'main')
    git(destination, 'add', '--all')
    git(destination, 'commit', '--quiet', '-m', 'Initial local product fixture')
    base = git(destination, 'rev-parse', 'HEAD')
    git(destination, 'update-ref', 'refs/remotes/origin/main', base)
    git(destination, 'symbolic-ref', 'refs/remotes/origin/HEAD', 'refs/remotes/origin/main')
    git(destination, 'switch', '--quiet', '-c', 'codex/local-review')
    if config:
        for relative, content in config['committed_files'].items():
            path = destination / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        git(destination, 'add', '--all')
        git(destination, 'commit', '--quiet', '-m', config['commit_subject'],
            timestamp='2026-10-12T00:01:00Z')
        if config['clean']:
            git(destination, 'update-ref', 'refs/remotes/origin/main',
                git(destination, 'rev-parse', 'HEAD'))
        copy_tree(source / 'app', destination)
    # Rubrics, TASK.md, case.json, and setup material are deliberately outside the workspace.
    return {'case': case_id, 'workspace': str(destination),
            'task_file': str(source / 'TASK.md'),
            'base': git(destination, 'rev-parse', 'origin/main'),
            'head': git(destination, 'rev-parse', 'HEAD'),
            'ahead': int(git(destination, 'rev-list', '--count', 'origin/main..HEAD')),
            'status': git(destination, 'status', '--porcelain').splitlines()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', required=True)
    parser.add_argument('--destination', required=True)
    args = parser.parse_args()
    print(json.dumps(prepare(args.case, args.destination), ensure_ascii=False, indent=2))
