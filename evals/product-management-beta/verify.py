#!/usr/bin/env python3
"""Verify recorded artifact integrity, not agent behavior or product quality."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]


def digest_file(path):
    return 'sha256:' + hashlib.sha256(path.read_bytes()).hexdigest()


def contained(root, relative):
    path = root / relative
    assert not Path(relative).is_absolute() and '..' not in Path(relative).parts
    assert path.resolve().is_relative_to(root.resolve()) and not path.is_symlink()
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence-root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--upstream-root', type=Path)
    args = parser.parse_args()
    evidence = args.evidence_root
    registry = json.loads((ROOT / 'skill-sources.json').read_text())
    spec = importlib.util.spec_from_file_location('source_compare', ROOT / 'skills/in-progress/upstream-sync/scripts/compare.py')
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    records = json.loads((evidence / 'trials.json').read_text())
    trials = records['trials']
    assert len(trials) == 11 and len({row['id'] for row in trials}) == 11
    for row in trials:
        task = contained(evidence, row['task'])
        assert digest_file(task) == row['taskDigest'], row['id'] + ': task drift'
        for path, expected in row['inputs'].items():
            input_path = task.parent / 'input' / path
            assert input_path.resolve().is_relative_to(task.parent.resolve())
            assert digest_file(input_path) == expected, row['id'] + ': input drift'
        assert row['artifacts'], row['id'] + ': no raw deliverable'
        for artifact in row['artifacts']:
            assert digest_file(contained(evidence, artifact['path'])) == artifact['sha256'], row['id'] + ': artifact drift'
        if row['skill']:
            snapshot = contained(evidence, row['snapshot'])
            assert helper.digest(helper.local_tree(evidence, row['snapshot'])) == row['skillDigest'], row['id'] + ': snapshot drift'
        else:
            assert row['snapshot'] is None and row['skillDigest'] is None
    for case in sorted({row['case'] for row in trials}):
        pair = [r for r in trials if r['case'] == case and r['arm'] in ('baseline', 'candidate')]
        assert len(pair) == 2
        assert pair[0]['taskDigest'] == pair[1]['taskDigest'] and pair[0]['inputs'] == pair[1]['inputs'], case + ': mismatched pair'
    repair = next(row for row in trials if row['arm'] == 'candidate-repair')
    first = next(row for row in trials if row['id'] == 'experiment-plan-candidate')
    assert repair['taskDigest'] == first['taskDigest'] and repair['inputs'] == first['inputs']
    assert repair['skillDigest'] != first['skillDigest']
    source_files = json.loads((evidence / 'upstream-files.json').read_text())
    upstream = {(row['source'], row['path']): row for row in source_files}
    for row in registry['skills']:
        if row['id'] not in ('problem-discovery', 'product-brief', 'experiment-design'):
            continue
        current_digest = helper.digest(helper.local_tree(ROOT, row['path']))
        current_trials = [r for r in trials if r['skill'] == row['id']]
        assert current_trials[-1]['skillDigest'] == current_digest, row['id'] + ': current skill not exercised'
        for origin in row['origins']:
            assert origin['localDigest'] == current_digest
            source_id = 'pm-skills' if origin['source'] == 'phuryn-pm-skills' else origin['source']
            for path, expected in origin['files'].items():
                item = upstream[(source_id, path)]
                assert item['sha256'] == expected and item['revision'] == origin['importedRevision'] == origin['reviewedRevision']
            notice = ROOT / row['path'] / ('LICENSE.' + source_id)
            assert digest_file(notice) == upstream[(source_id, 'LICENSE')]['sha256']
    if args.upstream_root:
        for row in source_files:
            assert digest_file(contained(args.upstream_root, row['source'] + '/' + row['path'])) == row['sha256'], row['path'] + ': upstream drift'
    print('Verified 11 trial records, five identical-input pairs, one repair, four immutable skill snapshots and direct-source/MIT hashes. Behavior verdicts remain evaluator-owned.')


if __name__ == '__main__':
    try:
        main()
    except (AssertionError, KeyError, OSError, ValueError) as error:
        print('Integrity check failed: ' + str(error), file=sys.stderr)
        sys.exit(1)
