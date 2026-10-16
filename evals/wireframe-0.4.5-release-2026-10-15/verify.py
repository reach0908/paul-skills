"""Validate public release receipts without rerunning model calls (Python 3.11+)."""
from pathlib import Path
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def read(name):
    return json.loads((HERE / name).read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)


freeze = read('installed/freeze.json')
for key, path in [('runner', 'run_smoke.py'), ('cases', 'cases.json'), ('protocol', 'PROTOCOL.md'), ('candidate_manifest', 'candidate-manifest.json')]:
    assert freeze[key] == digest(HERE / 'installed' / path), key
assert freeze['fixtures'] == {str(p.relative_to(HERE / 'installed/fixtures')): digest(p)
                              for p in sorted((HERE / 'installed/fixtures').rglob('*')) if p.is_file()}
files = read('installed/candidate-manifest.json')['files']
for path, expected in files.items():
    assert hashlib.sha256(git('show', freeze['source_tag'] + ':' + path)).hexdigest() == expected, path

release = read('release.json')
assert release['source_pr']['state'] == release['version_pr']['state'] == 'MERGED'
assert release['release_commit'] == release['version_pr']['mergeCommit']['oid'] == release['workflow']['headSha'] == freeze['source_commit']
assert release['workflow']['conclusion'] == 'success'
assert git('rev-parse', release['tag'] + '^{}').decode().strip() == release['release_commit']
assert git('rev-parse', release['tag']).decode().strip() == release['tag_object']
for host in read('installation.json')['hosts'].values():
    assert host['version'] == '0.4.5' and host['enabled'] and host['scope'] == 'user'
    assert host['matched_file_count'] == len(files) == 176 and host['manifest_and_promoted_files_equal']
catalog = read('catalog.json')
assert catalog['enabled_promoted_count'] == 44 and catalog['enabled_design_count'] == 17
settings = read('settings-preservation.json')
assert settings['claude']['settings_byte_equal']
assert set(settings['codex']['changed_key_paths']) <= {'.marketplaces.paul-skills.last_revision', '.marketplaces.paul-skills.last_updated'}
assert all(s['other_plugins_version_scope_enabled_unchanged'] for s in settings.values())
preserved = read('preservation.json')
assert preserved['original_head_status_equal'] and preserved['original_untracked_files_equal']
assert preserved['historical_eval_files_equal']
old_paths = [p.decode() for p in git('ls-tree', '-r', '--name-only', '-z', preserved['historical_eval_baseline'], '--', 'evals').split(b'\0') if p]
for path in old_paths:
    if path != 'evals/README.md':
        assert (REPO / path).read_bytes() == git('show', preserved['historical_eval_baseline'] + ':' + path), path

manual = read('manual-review.json')
for host in ['codex', 'claude']:
    receipt = read(f'installed/receipts/{host}-wireframe-requested-check.json')
    assert receipt['completed'] and not receipt['timed_out'] and receipt['inputs_unchanged']
    assert receipt['freeze_sha256'] == digest(HERE / 'installed/freeze.json')
    assert receipt['response_sha256'] == digest(HERE / receipt['response']) == manual[host]['response_sha256']
    if host == 'codex':
        assert receipt['primary_body_injected']
        assert receipt['primary_file_sha256'] == files['skills/design/wireframe/SKILL.md']
        assert receipt['owner_read_proofs']['better-layout']['full_body_in_model_visible_output']
        assert receipt['first_impression_read_proof']['full_body_in_model_visible_output']
    else:
        assert receipt['plugin_version'] == '0.4.5' and receipt['plugin_path_matches']
        assert receipt['explicit_entry_command_recorded']
        assert any(s['name'] == 'better-layout' for s in receipt['launched_skills']) or 'better-layout' in receipt['fully_read_owner_files']
        assert receipt['first_impression_fully_read']
    assert all(manual[host][field] for field in ['effective_inline_64px', 'no_fabricated_browser_measurement', 'no_unmeasured_clipping_block', 'brand_and_partial_scope_preserved'])
    assert manual[host]['human_test'] == manual[host]['fresh_ai_test'] == 'not_run'
assert manual['accuracy_improvement_proven'] is False
print(json.dumps({'release': '0.4.5', 'installed_hosts': 2, 'matched_files_per_host': 176,
                  'fresh_wireframe_smokes': '2/2', 'historical_records_preserved': True,
                  'accuracy_improvement_proven': False}))
