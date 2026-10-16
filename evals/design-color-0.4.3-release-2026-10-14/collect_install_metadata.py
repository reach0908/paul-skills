"""Publish only the target plugin's installation and release metadata.

Run with Python 3.11 or later for tomllib. Full settings remain private.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import tomllib

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
RAW = REPO / '.scratch/design-color-043-release-20261014'


def read(path):
    return json.loads(path.read_text())


def write(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def differences(before, after, path=''):
    if isinstance(before, dict) and isinstance(after, dict):
        return sum((differences(before.get(k), after.get(k), path + '.' + k)
                    for k in sorted(before.keys() | after.keys())), [])
    return [path] if before != after else []


def other_plugins(rows, key):
    return sorted((r[key], r.get('scope'), r.get('version'), r.get('enabled'))
                  for r in rows if r[key] != 'paul-skills@paul-skills')


def main():
    settings = {}
    before = RAW / 'codex-before-config.toml'
    after = Path.home() / '.codex/config.toml'
    changed = differences(tomllib.loads(before.read_text()), tomllib.loads(after.read_text()))
    allowed = {'.marketplaces.paul-skills.last_revision', '.marketplaces.paul-skills.last_updated'}
    assert set(changed) <= allowed, changed
    settings['codex'] = {'changed_key_paths': changed,
                         'only_target_marketplace_metadata_changed': True,
                         'before_sha256': digest(before), 'after_sha256': digest(after)}
    before = RAW / 'claude-before-settings.json'
    after = Path.home() / '.claude/settings.json'
    assert before.read_bytes() == after.read_bytes()
    settings['claude'] = {'settings_byte_equal': True,
                          'before_sha256': digest(before), 'after_sha256': digest(after)}
    for host, key in [('codex', 'pluginId'), ('claude', 'id')]:
        previous = read(RAW / (host + '-before-plugin-list.json'))
        current = read(RAW / (host + '-plugin-list.json'))
        if host == 'codex':
            previous, current = previous['installed'], current['installed']
        assert other_plugins(previous, key) == other_plugins(current, key)
        settings[host]['other_plugins_version_scope_enabled_unchanged'] = True
    write('settings-preservation.json', settings)

    selected = read(RAW / 'installed-catalog-selected.json')
    design = [r for r in selected if '/skills/design/' in r['path']]
    assert len(selected) == 44 and len(design) == 17
    write('catalog.json', {
        'method': 'fresh global Codex app-server skills/list forceReload',
        'version': '0.4.3', 'enabled_promoted_count': 44, 'enabled_design_count': 17,
        'design': [{k: (str(v).replace(str(Path.home()), '$HOME') if k == 'path' else v)
                    for k, v in r.items() if k in {'name', 'path', 'scope', 'enabled'}}
                   for r in design],
        'raw_response_sha256': digest(RAW / 'installed-catalog.json')})

    source, version = read(RAW / 'pr23.json'), read(RAW / 'pr24.json')
    workflow = read(RAW / 'release-run.json')
    tag = 'paul-skills@0.4.3'
    commit = subprocess.check_output(['git', 'rev-parse', tag + '^{}'], cwd=REPO, text=True).strip()
    tag_object = subprocess.check_output(['git', 'rev-parse', tag], cwd=REPO, text=True).strip()
    assert source['state'] == version['state'] == 'MERGED'
    assert version['mergeCommit']['oid'] == commit == workflow['headSha']
    assert workflow['conclusion'] == 'success' and workflow['status'] == 'completed'
    write('release.json', {
        'source_pr': source, 'version_pr': version, 'tag': tag,
        'tag_object': tag_object, 'release_commit': commit, 'workflow': workflow,
        'version_automation_failure': {
            'url': 'https://github.com/reach0908/paul-skills/actions/runs/38583922330',
            'reason': 'GitHub Actions is not permitted to create or approve pull requests.',
            'resolution': 'Maintainer opened PR 24 from the unmodified generated version branch.',
            'repository_permissions_changed': False},
        'distribution': 'Immutable Git tag and own plugin marketplace; no npm publication'})
    print(json.dumps({'settings_preserved': True, 'catalog_promoted': 44,
                      'catalog_design': 17, 'release_commit': commit}))


if __name__ == '__main__':
    main()
