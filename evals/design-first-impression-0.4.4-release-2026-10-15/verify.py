"""Check published receipt integrity; semantic judgments remain manual."""
from pathlib import Path
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def read(name):
    return json.loads((HERE / name).read_text())


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)


def main():
    freeze = read('freeze.json')
    for key, name in [('cases', 'cases.json'), ('protocol', 'PROTOCOL.md'),
                      ('runner', 'run_smoke.py'), ('release_files', 'candidate-manifest.json')]:
        assert sha((HERE / name).read_bytes()) == freeze[key], name
    actual = {str(p.relative_to(HERE / 'fixtures')): sha(p.read_bytes())
              for p in (HERE / 'fixtures').rglob('*') if p.is_file()}
    assert actual == freeze['fixtures']
    release, install = read('release.json'), read('installation.json')
    commit = release['release_commit']
    assert git('rev-parse', release['tag'] + '^{}').decode().strip() == commit == freeze['release_commit']
    assert git('rev-parse', release['tag']).decode().strip() == release['tag_object']
    assert release['source_pr']['state'] == release['version_pr']['state'] == 'MERGED'
    assert release['version_pr']['mergeCommit']['oid'] == release['workflow']['headSha'] == commit
    assert release['workflow']['conclusion'] == 'success'
    for pr in ['source_pr', 'version_pr']:
        assert release[pr]['statusCheckRollup'] and all(x['conclusion'] == 'SUCCESS' for x in release[pr]['statusCheckRollup'])
    expected = read('candidate-manifest.json')['files']
    assert expected == install['files'] and install['release_commit'] == commit
    for path, digest in expected.items():
        assert sha(git('show', commit + ':' + path)) == digest, path
    assert len(expected) == 176 and install['promoted_skills'] == 44
    assert all(x['version'] == '0.4.4' and x['enabled'] and x['manifest_equal']
               and x['all_promoted_files_equal'] for x in install['hosts'].values())
    catalog = read('catalog.json')
    assert catalog['enabled_promoted_count'] == 44 and catalog['enabled_design_count'] == 17
    preservation = read('preservation.json')
    assert not git('diff', '--name-only', preservation['source_head'], commit, '--', 'skills', 'evals').strip()
    assert preservation['original_checkout']['head_and_status_unchanged']
    assert preservation['original_checkout']['untracked_files_byte_equal']
    settings = read('settings-preservation.json')
    assert settings['codex']['only_target_marketplace_metadata_changed'] and settings['claude']['settings_byte_equal']
    assert all(x['other_plugins_version_scope_enabled_unchanged'] for x in settings.values())
    review = {(x['host'], x['case_id']): x for x in read('manual-review.json')['cases']}
    receipts = [read(str(p.relative_to(HERE))) for p in sorted((HERE / 'receipts').glob('*.json'))]
    cases = {x['id']: x for x in read('cases.json')}
    assert len(receipts) == 8 and {(r['host'], r['case_id']) for r in receipts} == set(review)
    for receipt in receipts:
        identity = receipt['host'], receipt['case_id']
        if receipt['status'] == 'not_run':
            assert identity[0] == 'codex' and receipt['case_id'] in read('codex-stop.json')['unstarted']
            assert review[identity]['target_contract'] == 'not_run'
            continue
        assert receipt['inputs_unchanged'] and receipt['files_before'] == receipt['files_after']
        fixture = cases[receipt['case_id']]['fixture']
        expected_fixture = {p.split('/', 1)[1]: digest for p, digest in actual.items() if p.startswith(fixture + '/')}
        assert expected_fixture == receipt['files_before']
        assert receipt['freeze_sha256'] == sha((HERE / 'freeze.json').read_bytes())
        if identity[0] == 'codex':
            assert receipt['status'] == 'execution_failed' and receipt['selected_skill_exact_body_injected']
            assert 'requires a newer version of Codex' in receipt['failure']
            assert review[identity]['target_contract'] == 'not_run'
            continue
        assert receipt['completed'] and receipt['plugin_version'] == '0.4.4'
        assert receipt['plugin_path_matches'] and receipt['explicit_entry_command_recorded']
        assert sha((HERE / receipt['response']).read_bytes()) == receipt['response_sha256'] == review[identity]['response_sha256']
        if receipt['case_id'] == 'staged':
            assert not receipt['tool_calls']
        else:
            assert receipt['first_impression_fully_read']
        if receipt['case_id'] == 'warning':
            assert receipt['audit_procedure_fully_read'] and receipt['all_six_owners_before_artifact']
        if receipt['case_id'] == 'wireframe-requested-check':
            assert any(x['name'] == 'better-layout' for x in receipt['launched_skills'])
    assert review['claude', 'wireframe-requested-check']['target_contract'] == 'pass_with_ancillary_error'
    assert sum(r['status'] == 'completed' for r in receipts) == 4
    assert sum(r['status'] == 'execution_failed' for r in receipts) == 2
    assert sum(r['status'] == 'not_run' for r in receipts) == 2
    print(json.dumps({'integrity': 'pass', 'claude_completed': 4, 'codex_failed': 2,
                      'codex_not_run': 2, 'ancillary_response_errors_retained': 1,
                      'human_three_second_validation': 'not_run'}))


if __name__ == '__main__':
    main()
