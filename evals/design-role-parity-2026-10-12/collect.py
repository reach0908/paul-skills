#!/usr/bin/env python3
"""Record artifacts and input preservation without assigning quality scores."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = ROOT / '.scratch/design-role-parity-20261012'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def collect(run):
    folder = BASE / 'runs' / run
    manifest = json.loads((folder / 'trial.json').read_text())
    changed = []
    missing = []
    for name, before in manifest['inputs'].items():
        p = folder / name
        if not p.exists():
            missing.append(name)
        elif sha(p) != before:
            changed.append(name)
    cases = []
    for case in manifest['cases']:
        directory = folder / 'cases' / case['id']
        execution = directory / 'output/execution.json'
        report = directory / 'output/report.md'
        # The single-case supplement prompt explicitly uses run-level output.
        if manifest.get('kind') == 'supplement' and len(manifest['cases']) == 1:
            execution = folder / 'output/execution.json'
            report = folder / 'output/report.md'
        entry = {'id': case['id'], 'reportPresent': report.is_file(),
                 'executionPresent': execution.is_file(), 'status': 'not recorded',
                 'reportPath': str(report.relative_to(folder)),
                 'executionPath': str(execution.relative_to(folder))}
        if execution.is_file():
            try:
                entry['execution'] = json.loads(execution.read_text())
                entry['status'] = entry['execution'].get('status', 'unknown')
            except (ValueError, OSError) as exc:
                entry['parseError'] = str(exc)
        cases.append(entry)
    outputs = {str(p.relative_to(folder)): sha(p) for p in sorted(folder.rglob('*'))
               if p.is_file() and '.git' not in p.parts and '.agents' not in p.parts
               and p.name not in ('receipt.json',)}
    result = {'id': run, 'role': manifest['role'], 'arm': manifest['arm'],
              'repeat': manifest['repeat'], 'cases': cases,
              'changedInputs': changed, 'missingInputs': missing,
              'skillsUnchanged': not any(x.startswith('.agents/') for x in changed + missing),
              'artifactHashes': outputs,
              'qualityDecision': 'requires independent adjudication'}
    (folder / 'receipt.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    return {'id': run, 'cases': [x['status'] for x in cases],
            'skillsUnchanged': result['skillsUnchanged'],
            'changedInputs': len(changed), 'missingInputs': len(missing)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('runs', nargs='*')
    args = parser.parse_args()
    runs = args.runs or [p.name for p in sorted((BASE / 'runs').iterdir()) if (p / 'trial.json').exists()]
    for run in runs:
        print(json.dumps(collect(run)))
