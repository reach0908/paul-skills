"""Verify frozen inputs, source application and hash-bound review evidence."""
from pathlib import Path
import hashlib, json, subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def read(path):
    return json.loads((HERE / path).read_text())


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)


def check_freeze(group):
    frozen = read(group + '/freeze.json')
    runner = 'run_trials.py' if group == 'comparison' else 'run_smoke.py'
    for key, name in [('protocol', 'PROTOCOL.md'), ('cases', 'cases.json'), ('runner', runner)]:
        assert sha((HERE / group / name).read_bytes()) == frozen[key], (group, name)
    fixtures = HERE / group / 'fixtures'
    actual = {str(p.relative_to(fixtures)): sha(p.read_bytes()) for p in fixtures.rglob('*') if p.is_file()}
    assert actual == frozen['fixtures']
    return frozen


def check_receipt(group, receipt):
    frozen = read(group + '/freeze.json')
    assert receipt['completed'] and receipt['exit_code'] == 0 and not receipt['timed_out']
    assert receipt['inputs_unchanged'] and receipt['files_before'] == receipt['files_after']
    assert receipt['freeze_sha256'] == sha((HERE / group / 'freeze.json').read_bytes())
    assert sha((HERE / receipt['response']).read_bytes()) == receipt['response_sha256']
    cases = {c['id']: c for c in read(group + '/cases.json')}
    prefix = cases[receipt['case_id']]['fixture'] + '/'
    expected = {p[len(prefix):]: digest for p, digest in frozen['fixtures'].items() if p.startswith(prefix)}
    assert expected == receipt['files_before']


def main():
    cli = read('cli-repair.json')
    assert cli['before_version'] == '0.146.0' and cli['after_version'] == '0.162.1'
    assert not cli['probes']['before']['passed'] and cli['probes']['after']['passed']
    assert cli['probes']['before']['actual_model'] == cli['probes']['after']['actual_model'] == 'gpt-6-astra'
    assert cli['other_npm_packages_unchanged'] and all(s['byte_equal'] for s in cli['settings'].values())
    for group in ['installed', 'reproduction', 'comparison']:
        check_freeze(group)
    frozen = read('comparison/freeze.json')
    changed = [p for p in frozen['arms']['baseline'] if frozen['arms']['baseline'].get(p) != frozen['arms']['candidate'].get(p)]
    assert set(frozen['arms']['baseline']) == set(frozen['arms']['candidate'])
    assert changed == ['skills/design/wireframe/SKILL.md']
    for path, digest in frozen['arms']['baseline'].items():
        assert sha(git('show', frozen['base'] + ':' + path)) == digest
    assert sha((REPO / changed[0]).read_bytes()) == frozen['arms']['candidate'][changed[0]]
    oracle = read('css-oracle.json')
    assert sha((HERE / 'css-oracle-run.js').read_bytes()) == oracle['script_sha256']
    expected = {('inline', 1040): '64px', ('inline', 360): '64px', ('important', 1040): '64px',
                ('important', 360): '30px', ('stylesheet', 1040): '38px', ('stylesheet', 360): '30px'}
    assert len(oracle['results']) == 6
    assert {(r['case'], r['viewport']['width']): r['computed'] for r in oracle['results']} == expected
    for case, digest in oracle['fixture_sha256'].items():
        assert sha((HERE / f'comparison/fixtures/{case}/index.html').read_bytes()) == digest
    review = read('manual-review.json')
    installed = {p.stem.removeprefix('codex-'): read(str(p.relative_to(HERE))) for p in (HERE / 'installed/receipts').glob('*.json')}
    assert len(installed) == 4
    for case, receipt in installed.items():
        check_receipt('installed', receipt)
        assert receipt['host_version'] == '0.162.1' and receipt['primary_body_injected']
        assert receipt['actual_model'] == 'gpt-6-astra' and receipt['actual_effort'] == 'low'
        manual = next(r for r in review['installed'] if r['case_id'] == case)
        assert manual['response_sha256'] == receipt['response_sha256'] and manual['target_contract'] == 'pass'
        if case == 'staged':
            assert receipt['first_artifact_read_event'] is None and not receipt['owner_read_proofs']
            assert len(receipt['tool_calls']) == 1 and '/better-interface/SKILL.md' in receipt['tool_calls'][0]['input']
        else:
            assert receipt['first_impression_read_proof'] and 'better-layout' in receipt['owner_read_proofs']
    warning = installed['warning']
    assert warning['audit_procedure_read_proof'] and warning['all_six_owners_before_artifact']
    assert warning['audit_procedure_read_proof']['result_event'] < min(p['call_event'] for p in warning['owner_read_proofs'].values())
    diagnostic = read('reproduction/receipts/claude-wireframe-requested-check.json')
    check_receipt('reproduction', diagnostic)
    assert review['diagnostic']['response_sha256'] == diagnostic['response_sha256']
    assert not review['diagnostic']['css_error_reproduced'] and review['diagnostic']['unmeasured_overflow_blocked']
    assert len(review['comparison']) == 8
    for manual in review['comparison']:
        receipt = read(f"comparison/receipts/{manual['arm']}-{manual['case_id']}.json")
        check_receipt('comparison', receipt)
        assert receipt['plugin_path_matches'] and receipt['explicit_entry_command_recorded']
        assert receipt['first_impression_fully_read'] and any(x['name'] == 'better-layout' for x in receipt['launched_skills'])
        assert manual['response_sha256'] == receipt['response_sha256']
        fixture = next(c['fixture'] for c in read('comparison/cases.json') if c['id'] == manual['case_id'])
        assert str(manual['effective_mobile_title_px']) + 'px' == expected[fixture, 360]
        assert manual['css_value'] == 'correct' and not manual['unmeasured_clipping_blocked']
    preserve = read('preservation.json')
    prior_changes = git('diff', '--name-only', preserve['baseline'], '--', 'evals').decode().splitlines()
    assert all(p == 'evals/README.md' or p.startswith('evals/design-cli-css-repair-2026-10-15/') for p in prior_changes)
    assert preserve['original_checkout_head_and_status_equal'] and preserve['original_untracked_files_equal']
    assert preserve['settings_unchanged'] and preserve['candidate_not_installed_globally']
    print(json.dumps({'integrity': 'pass', 'installed_contracts': '4/4', 'paired_css_values': {'baseline': '4/4', 'candidate': '4/4'},
                      'diagnostic_blocking_failure_preserved': True, 'accuracy_improvement_proven': False}))


if __name__ == '__main__':
    main()
