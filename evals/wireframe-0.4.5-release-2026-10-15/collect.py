"""Export bounded release evidence; full host context stays in ignored scratch."""
from pathlib import Path
import hashlib
import importlib.util
import json
import subprocess
import tomllib

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
RAW = REPO / '.scratch/wireframe-045-release'
TAG = 'paul-skills@0.4.5'


def read(path):
    return json.loads(path.read_text())


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def git(*args, cwd=REPO):
    return subprocess.check_output(['git', *args], cwd=cwd)


def differences(before, after, path=''):
    if isinstance(before, dict) and isinstance(after, dict):
        return sum((differences(before.get(k), after.get(k), path + '.' + k)
                    for k in sorted(before.keys() | after.keys())), [])
    return [path] if before != after else []


def metadata():
    files = read(HERE / 'installed/candidate-manifest.json')['files']
    hosts = {}
    settings = {}
    for host, key in [('codex', 'pluginId'), ('claude', 'id')]:
        before = read(RAW / f'{host}-before-plugin-list.json')
        after = read(RAW / f'{host}-plugin-list.json')
        if host == 'codex':
            before, after = before['installed'], after['installed']
        other = lambda rows: sorted((p[key], p.get('scope'), p.get('version'), p.get('enabled'))
                                    for p in rows if p[key] != 'paul-skills@paul-skills')
        assert other(before) == other(after)
        plugin = next(p for p in after if p[key] == 'paul-skills@paul-skills')
        cache = Path(read(RAW / 'codex-plugin-add.json')['installedPath'] if host == 'codex' else plugin['installPath'])
        assert plugin['version'] == '0.4.5' and plugin['enabled']
        if host == 'claude':
            assert plugin['scope'] == 'user'
        for path, digest in files.items():
            assert sha((cache / path).read_bytes()) == digest, (host, path)
            assert sha(git('show', TAG + ':' + path)) == digest, path
        hosts[host] = {'version': '0.4.5', 'enabled': True, 'scope': 'user',
                       'cache': str(cache).replace(str(Path.home()), '$HOME'),
                       'manifest_and_promoted_files_equal': True, 'matched_file_count': len(files)}
        settings[host] = {'other_plugins_version_scope_enabled_unchanged': True}

    before = RAW / 'codex-before-config.toml'
    after = Path.home() / '.codex/config.toml'
    changed = differences(tomllib.loads(before.read_text()), tomllib.loads(after.read_text()))
    assert set(changed) <= {'.marketplaces.paul-skills.last_revision', '.marketplaces.paul-skills.last_updated'}, changed
    settings['codex'].update(changed_key_paths=changed, before_sha256=sha(before.read_bytes()), after_sha256=sha(after.read_bytes()))
    before = RAW / 'claude-before-settings.json'
    after = Path.home() / '.claude/settings.json'
    assert before.read_bytes() == after.read_bytes()
    settings['claude'].update(settings_byte_equal=True, before_sha256=sha(before.read_bytes()), after_sha256=sha(after.read_bytes()))
    write('settings-preservation.json', settings)
    write('installation.json', {'tag': TAG, 'release_commit': git('rev-parse', TAG + '^{}').decode().strip(), 'promoted_skills': 44, 'hosts': hosts})

    original = Path.home() / 'dev/paul-skills'
    previous = read(RAW / 'original-before.json')
    files = {p.decode(): sha((original / p.decode()).read_bytes())
             for p in git('ls-files', '--others', '--exclude-standard', '-z', cwd=original).split(b'\0') if p}
    assert previous['head'] == git('rev-parse', 'HEAD', cwd=original).decode().strip()
    assert previous['status'] == git('status', '--porcelain=v1', '-b', cwd=original).decode()
    assert previous['untracked'] == files
    # Compare every evaluation file present at the source PR head, excluding only
    # the index, which may gain a new report link. No historical outputs are edited.
    old = '4e7a8ca47810ec5c04dac2418fa5bec61d28c6be'
    old_paths = [p.decode() for p in git('ls-tree', '-r', '--name-only', '-z', old, '--', 'evals').split(b'\0') if p]
    old_paths = [p for p in old_paths if p != 'evals/README.md']
    for path in old_paths:
        assert (REPO / path).read_bytes() == git('show', old + ':' + path), path
    write('preservation.json', {'original_head': previous['head'], 'original_head_status_equal': True,
                               'original_untracked_files_equal': True, 'original_untracked_count': len(files),
                               'historical_eval_baseline': old, 'historical_eval_files_equal': True,
                               'historical_eval_file_count': len(old_paths)})

    source, version = read(RAW / 'pr29.json'), read(RAW / 'pr30.json')
    workflow = read(RAW / 'release-run.json')
    commit = git('rev-parse', TAG + '^{}').decode().strip()
    assert source['state'] == version['state'] == 'MERGED'
    assert version['mergeCommit']['oid'] == commit == workflow['headSha']
    assert workflow['conclusion'] == 'success'
    write('release.json', {'source_pr': source, 'version_pr': version, 'tag': TAG,
                          'tag_object': git('rev-parse', TAG).decode().strip(), 'release_commit': commit,
                          'workflow': workflow, 'version_pr_automation_failure': {
                              'url': 'https://github.com/reach0908/paul-skills/actions/runs/38753655750',
                              'reason': 'GitHub Actions is not permitted to create or approve pull requests.',
                              'resolution': 'Maintainer opened PR 30 from the unmodified generated version branch.',
                              'repository_permissions_changed': False},
                          'distribution': 'Namespaced Git tag and own marketplace; no npm publication'})


def catalog():
    selected = read(RAW / 'installed-catalog-selected.json')
    design = [s for s in selected if '/skills/design/' in s['path']]
    assert len(selected) == 44 and len(design) == 17
    write('catalog.json', {'method': 'fresh global Codex app-server skills/list forceReload', 'version': '0.4.5',
                           'enabled_promoted_count': len(selected), 'enabled_design_count': len(design),
                           'raw_response_sha256': sha((RAW / 'installed-catalog.json').read_bytes()),
                           'design': [{k: (v.replace(str(Path.home()), '$HOME') if k == 'path' else v)
                                       for k, v in s.items() if k in {'name', 'path', 'scope', 'enabled'}} for s in design]})


def smoke():
    spec = importlib.util.spec_from_file_location('prior_collector', HERE.parent / 'design-cli-css-repair-2026-10-15/collect.py')
    collector = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(collector)
    collector.HERE = HERE
    cases = read(HERE / 'installed/cases.json')
    for host in ['codex', 'claude']:
        for case in cases:
            print(json.dumps(collector.collect('installed', RAW / 'installed' / host / case['id'], host, case)))


if __name__ == '__main__':
    import sys
    {'metadata': metadata, 'catalog': catalog, 'smoke': smoke}[sys.argv[1]]()
