#!/usr/bin/env python3
"""Read-only, pinned three-way skill inventory. No fetch, apply, or state writes."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys


def git(repo, *args):
    return subprocess.check_output(
        ['git', '--no-pager', '-c', 'core.fsmonitor=false', '-c', 'core.hooksPath=/dev/null', '-C', str(repo), *args],
        stderr=subprocess.PIPE, env={**os.environ, 'GIT_OPTIONAL_LOCKS': '0'},
    )


def revision(repo, value):
    if not isinstance(value, str) or not re.fullmatch(r'[0-9a-f]{40}', value):
        raise ValueError('A full 40-character commit ID is required')
    if git(repo, 'cat-file', '-t', value).strip() != b'commit':
        raise ValueError('Revision is not a commit')
    return value


def relative(value):
    if not isinstance(value, str) or not value or '\\' in value or '\0' in value:
        raise ValueError('Invalid relative path')
    path = PurePosixPath(value)
    if path.is_absolute() or '..' in path.parts or str(path) != value or value == '.':
        raise ValueError('Path must be normalized and contained in its repository')
    return value


def digest(tree):
    data = json.dumps(sorted((p, *v) for p, v in tree.items()), separators=(',', ':'), ensure_ascii=True)
    return 'sha256:' + hashlib.sha256(data.encode()).hexdigest()


def local_tree(root, path):
    relative(path)
    root = Path(root).resolve()
    folder = root / path
    for parent in [folder, *folder.parents]:
        if parent == root:
            break
        if parent.is_symlink():
            raise ValueError('Local symlinks are unsupported')
    if not folder.resolve().is_relative_to(root) or not folder.is_dir():
        raise ValueError('Local skill directory is missing or outside the workspace')
    tree = {}
    for file in sorted(folder.rglob('*')):
        if file.is_symlink():
            raise ValueError('Local symlinks are unsupported')
        if file.is_dir():
            continue
        if not file.is_file():
            raise ValueError('Unsupported local file')
        mode = '100755' if file.stat().st_mode & 0o111 else '100644'
        tree[file.relative_to(folder).as_posix()] = (mode, hashlib.sha256(file.read_bytes()).hexdigest())
    if 'SKILL.md' not in tree:
        raise ValueError('Local SKILL.md is missing')
    return tree


def source_tree(repo, rev, path):
    relative(path)
    prefix = path + '/'
    tree = {}
    for entry in git(repo, 'ls-tree', '-rz', rev, '--', prefix).split(b'\0'):
        if not entry:
            continue
        info, raw_path = entry.split(b'\t', 1)
        mode, kind, oid = info.decode().split()
        if kind != 'blob' or mode not in ('100644', '100755'):
            raise ValueError('Source symlinks and submodules are unsupported')
        name = raw_path.decode('utf-8')
        if not name.startswith(prefix):
            raise ValueError('Unexpected source path')
        tree[name[len(prefix):]] = (mode, hashlib.sha256(git(repo, 'cat-file', 'blob', oid)).hexdigest())
    if 'SKILL.md' not in tree:
        raise ValueError('Source SKILL.md is missing; inspect rename/deletion evidence')
    return tree


def changes(before, after):
    return [{'path': p, 'change': 'added' if p not in before else 'deleted' if p not in after else 'modified'}
            for p in sorted(before.keys() | after.keys()) if before.get(p) != after.get(p)]


def report(registry, source_id, upstream, target, local_root):
    if registry.get('schemaVersion') != 1:
        raise ValueError('Unsupported registry schemaVersion')
    source = registry['sources'][source_id]
    revision(upstream, target)
    result = {'source': source_id, 'repository': source['repository'], 'target': target,
              'freshness': 'pinned-checkout-only; verify remote separately', 'skills': [], 'status': 'COMPARED'}
    review = source.get('repositoryReview')
    if review:
        revision(upstream, review)
        result['repositoryBase'] = review
        result['repositoryChanges'] = git(upstream, 'diff', '--name-status', '--find-renames', review, target, '--').decode()
        result['commits'] = git(upstream, 'log', '--format=%h %s', review + '..' + target, '--').decode().splitlines()
    else:
        result['repositoryChanges'] = None
        result['repositoryReviewStatus'] = 'UNKNOWN'
        result['status'] = 'UNKNOWN'
    known = set()
    for skill in registry['skills']:
        for origin in skill.get('origins', []):
            if origin['source'] != source_id:
                continue
            path = origin.get('reviewPath', origin['path'])
            known.add(path)
            row = {'id': skill['id'], 'localPath': skill['path'], 'sourcePath': path,
                   'base': origin.get('reviewedRevision') or origin.get('importedRevision')}
            try:
                base = revision(upstream, row['base'])
                if subprocess.run(['git', '-C', str(upstream), 'merge-base', '--is-ancestor', base, target],
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0:
                    raise ValueError('Target does not descend from baseline; review rewritten history')
                old = source_tree(upstream, base, path)
                new = source_tree(upstream, target, path)
                local = local_tree(local_root, skill['path'])
                row.update(localDigest=digest(local), upstreamChanges=changes(old, new),
                           localChanges=changes(old, local), differencesFromTarget=changes(new, local),
                           pending=[d for d in origin.get('decisions', []) if d.get('decision') == 'defer'])
                row['localDrift'] = None if not origin.get('localDigest') else origin['localDigest'] != row['localDigest']
                row['status'] = 'REVIEW' if row['upstreamChanges'] or row['pending'] or row['localDrift'] is not False else 'UNCHANGED'
            except (KeyError, ValueError, OSError, subprocess.CalledProcessError) as exc:
                row.update(status='UNKNOWN', error=str(exc))
                result['status'] = 'UNKNOWN'
            result['skills'].append(row)
    names = git(upstream, 'ls-tree', '-rz', '--name-only', target).decode().split('\0')
    result['newCandidates'] = sorted(str(PurePosixPath(p).parent) for p in names if p.endswith('/SKILL.md') and str(PurePosixPath(p).parent) not in known)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('registry', 'source', 'upstream', 'target', 'local-root'):
        parser.add_argument('--' + name, required=True)
    args = parser.parse_args()
    try:
        data = report(json.loads(Path(args.registry).read_text()), args.source, args.upstream, args.target, args.local_root)
    except (KeyError, ValueError, OSError, subprocess.CalledProcessError) as exc:
        data = {'status': 'UNKNOWN', 'error': str(exc)}
    print(json.dumps(data, indent=2))
    return 2 if data['status'] == 'UNKNOWN' else 0


if __name__ == '__main__':
    sys.exit(main())
