#!/usr/bin/env python3
"""Verify the complete public receipt set without starting any model runs."""
import argparse
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify():
    config = json.loads((HERE / 'cases.json').read_text())
    cases = config['cases']
    summary = json.loads((HERE / 'evidence/summary.json').read_text())
    assert len(cases) == 34 and len({c['id'] for c in cases}) == 34
    assert summary['completed'] == 34, 'Incomplete matrix'
    assert summary['installation']['all_equal']
    rows = []
    sessions = set()
    protocol_hash = sha(HERE / 'PROTOCOL-2.md')
    cases_hash = sha(HERE / 'cases.json')
    names = {c['expected'] for c in cases if c['mode'] == 'explicit'}
    automatic = names - set(config['user_only'])
    for i, case in enumerate(cases, 1):
        row = json.loads((HERE / 'evidence' / (case['id'] + '.json')).read_text())
        assert all(row[k] == case[k] for k in ['mode', 'expected', 'prompt'])
        assert row['case_id'] == case['id']
        assert row['protocol_version'] == 2 and row['protocol_sha256'] == protocol_hash
        assert row['cases_sha256'] == cases_hash
        assert row['trial_directory_name'] == f'case_{i:03d}'
        assert row['session_id'] not in sessions, 'Reused conversation'
        sessions.add(row['session_id'])
        assert set(row['automatic_design_catalog']) == automatic
        assert set(row['direct_design_catalog']) == names
        assert set(row['available_tools']) == {'Skill', 'Read', 'Glob', 'Grep'}
        assert row['pass'] == all(row['checks'].values()), 'Inconsistent verdict'
        assert row['actual_billed_usd'] is None
        for key in ['stream_sha256', 'transcript_sha256']:
            assert re.fullmatch(r'[0-9a-f]{64}', row[key])
        rows.append(row)
    assert summary['passed'] == sum(r['pass'] for r in rows)
    for mode, group in summary['by_mode'].items():
        assert group['completed'] == sum(r['mode'] == mode for r in rows)
        assert group['passed'] == sum(r['mode'] == mode and r['pass'] for r in rows)
    total = sum(r['reported_cost_usd'] for r in rows)
    assert abs(total - summary['reported_matrix_cost_usd']) < 1e-8
    exploration = json.loads((HERE / 'exploratory-evidence/summary.json').read_text())
    calibration = json.loads((HERE / 'evidence/calibration.json').read_text())
    all_phases = summary['all_phases']
    assert all_phases['total_model_runs'] == 47
    assert all_phases['excluded_exploratory_runs'] == exploration['completed'] == 12
    assert abs(all_phases['total_reported_cost_usd'] - total - exploration['reported_cost_usd'] - calibration['reported_cost_usd']) < 1e-8
    assert all_phases['actual_billed_usd'] is None
    assert all_phases['answer_based_rerolls'] == 0
    return {'receipts': len(rows), 'passed': summary['passed'],
            'separate_conversations': len(sessions),
            'total_model_runs_including_exclusions': 47,
            'reported_list_cost_usd': all_phases['total_reported_cost_usd']}


def files():
    return {str(p.relative_to(HERE)): sha(p) for p in sorted(HERE.rglob('*'))
            if p.is_file() and '__pycache__' not in p.parts and p.name != 'MANIFEST.json'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write-manifest', action='store_true')
    args = parser.parse_args()
    result = verify()
    manifest = HERE / 'MANIFEST.json'
    if args.write_manifest:
        manifest.write_text(json.dumps({'sha256': files()}, ensure_ascii=False, indent=2) + '\n')
    assert json.loads(manifest.read_text())['sha256'] == files(), 'Public evidence changed'
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
