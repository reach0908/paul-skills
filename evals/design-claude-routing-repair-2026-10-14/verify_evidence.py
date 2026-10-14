#!/usr/bin/env python3
"""Check frozen inputs and public receipt consistency without running a model."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    config = json.loads((HERE / 'cases.json').read_text())
    summary = json.loads((HERE / 'evidence/summary.json').read_text())
    bundle = json.loads((HERE / 'bundle-manifest.json').read_text())
    cases = config['cases']
    assert len(cases) == 46 and len({c['id'] for c in cases}) == 46
    old = json.loads((HERE.parent / 'design-claude-discovery-2026-10-14/cases.json').read_text())
    current = {c['id']: c for c in cases}
    for c in old['cases']:
        assert c['prompt'] == current[c['id']]['prompt'], c['id']
    for path, expected in bundle['files'].items():
        source = HERE / 'diagnostics/candidate-1-better-interface.txt' if path == 'skills/design/better-interface/SKILL.md' else REPO / path
        if path == '.claude-plugin/plugin.json':
            source = HERE / 'diagnostics/plugin-0.4.0.json'
        assert sha(source) == expected, f'Candidate drift: {path}'
    rows = []
    for c in cases:
        r = json.loads((HERE / 'evidence' / (c['id'] + '.json')).read_text())
        assert r['case_id'] == c['id'] and r['prompt'] == c['prompt']
        assert r['arm'] == c['arm']
        assert r['protocol_sha256'] == sha(HERE / 'PROTOCOL.md')
        assert r['cases_sha256'] == sha(HERE / 'cases.json')
        assert r['bundle_manifest_sha256'] == sha(HERE / 'bundle-manifest.json')
        assert re.fullmatch(r'case_\d{3}', r['trial_directory_name'])
        assert r['pass'] == all(r['checks'].values())
        assert r['actual_billed_usd'] is None
        for b in r['full_body_loads']:
            if c['arm'] == 'candidate':
                assert b['file_sha256'] == bundle['files'][f"skills/design/{b['name']}/SKILL.md"]
        rows.append(r)
    assert len({r['session_id'] for r in rows}) == 46
    assert summary['completed'] == 46
    for arm in ['candidate', 'baseline']:
        arm_rows = [r for r in rows if r['arm'] == arm]
        assert summary['by_arm'][arm] == {'completed': len(arm_rows), 'passed': sum(r['pass'] for r in arm_rows)}
    assert abs(summary['reported_cost_usd'] - sum(r['reported_cost_usd'] or 0 for r in rows)) < 1e-8
    before = json.loads((HERE / 'installation-before.json').read_text())
    assert before['all_equal'] and len(before['files']) == 34
    for row in before['files']:
        original = subprocess.check_output(['git', 'show', 'paul-skills@0.4.0:' + row['path']], cwd=REPO)
        assert hashlib.sha256(original).hexdigest() == row['installed_sha256'], row['path']
    follow = HERE / 'recovery'
    final_bundle = json.loads((follow / 'bundle-manifest.json').read_text())
    changed = [p for p in bundle['files'] if bundle['files'][p] != final_bundle['files'][p]]
    assert changed == ['skills/design/better-interface/SKILL.md']
    for path, expected in final_bundle['files'].items():
        source = HERE / 'diagnostics/plugin-0.4.0.json' if path == '.claude-plugin/plugin.json' else REPO / path
        assert sha(source) == expected, f'Final source drift: {path}'
    follow_cases = json.loads((follow / 'cases.json').read_text())['cases']
    assert len(follow_cases) == 13
    follow_rows = []
    for c in follow_cases:
        r = json.loads((follow / 'evidence' / (c['id'] + '.json')).read_text())
        assert r['prompt'] == c['prompt'] and r['case_id'] == c['id']
        assert r['protocol_sha256'] == sha(follow / 'PROTOCOL.md')
        assert r['cases_sha256'] == sha(follow / 'cases.json')
        assert r['bundle_manifest_sha256'] == sha(follow / 'bundle-manifest.json')
        assert r['pass'] == all(r['checks'].values())
        for b in r['full_body_loads']:
            assert b['file_sha256'] == final_bundle['files'][f"skills/design/{b['name']}/SKILL.md"]
        follow_rows.append(r)
    assert len({r['session_id'] for r in rows + follow_rows}) == 59
    follow_summary = json.loads((follow / 'evidence/summary.json').read_text())
    assert follow_summary['completed'] == 13
    assert follow_summary['by_arm']['candidate']['passed'] == sum(r['pass'] for r in follow_rows)
    assert abs(follow_summary['reported_cost_usd'] - sum(r['reported_cost_usd'] or 0 for r in follow_rows)) < 1e-8
    forbidden = [r'/Users/[^/]+/', r'(?i)sk-ant-[a-z0-9_-]{10,}', r'gh[pousr]_[A-Za-z0-9]{20,}']
    for f in HERE.rglob('*'):
        if f.is_file() and f.suffix in {'.json', '.md'}:
            text = f.read_text()
            assert '\u2014' not in text, f'Literal em dash: {f}'
            assert not any(re.search(pattern, text) for pattern in forbidden), f'Private data: {f}'
    manifest = json.loads((HERE / 'MANIFEST.json').read_text())
    actual = {str(p.relative_to(HERE)) for p in HERE.rglob('*') if p.is_file() and p.name != 'MANIFEST.json' and '__pycache__' not in p.parts}
    assert actual == set(manifest['files'])
    for path, expected in manifest['files'].items():
        assert sha(HERE / path) == expected, path
    print(json.dumps({'sessions': len(rows) + len(follow_rows), 'initial_outcomes': summary['by_arm'], 'final_followup': follow_summary['by_arm'], 'historical_install_matches_0_4_0_tag': True, 'frozen_sources_equal': True, 'manifest_files': len(actual)}))


if __name__ == '__main__':
    main()
