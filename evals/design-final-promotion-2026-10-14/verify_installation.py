"""Compare both global installs and a fresh catalog with the exact release tag."""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / 'evidence'
RAW = ROOT / '.scratch/design-final-release-20261014'
TAG = 'paul-skills@0.4.0'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def sha(content):
    return hashlib.sha256(content).hexdigest()

commit = git('rev-parse', TAG + '^{}').decode().strip()
manifest_bytes = git('show', TAG + ':.claude-plugin/plugin.json')
manifest = json.loads(manifest_bytes)
assert manifest['version'] == '0.4.0' and len(manifest['skills']) == 44
codex = next(p for p in json.loads((RAW / 'codex-plugin-list.json').read_text())['installed']
             if p['pluginId'] == 'paul-skills@paul-skills')
claude = next(p for p in json.loads((RAW / 'claude-plugin-list.json').read_text())
              if p['id'] == 'paul-skills@paul-skills' and p['scope'] == 'user')
assert codex['version'] == claude['version'] == '0.4.0'
assert codex['enabled'] and claude['enabled']
assert codex['marketplaceSource']['source'] == 'https://github.com/reach0908/paul-skills.git'
paths = [p.decode() for p in git('ls-tree', '-r', '--name-only', '-z', TAG, '--',
         *[p.removeprefix('./') for p in manifest['skills']]).split(b'\0') if p]
files = [{'path': p, 'sha256': sha(git('show', TAG + ':' + p))} for p in paths]
hosts = {}
for name, cache in [('codex', Path(json.loads((RAW / 'codex-plugin-add.json').read_text())['installedPath'])),
                    ('claude', Path(claude['installPath']))]:
    assert sha((cache / '.claude-plugin/plugin.json').read_bytes()) == sha(manifest_bytes)
    for row in files:
        assert sha((cache / row['path']).read_bytes()) == row['sha256'], (name, row['path'])
    hosts[name] = {'version': '0.4.0', 'enabled': True, 'scope': 'user', 'promotedSkills': 44,
                   'verifiedSkillFiles': len(files), 'cachePath': str(cache),
                   'manifestSha256': sha(manifest_bytes), 'status': 'pass'}
catalog = json.loads((ROOT / '.scratch/design-final-promotion-20261014/installed-catalog-selected.json').read_text())
assert len(catalog) == 44 and all(s['enabled'] for s in catalog)
assert all('/paul-skills/paul-skills/0.4.0/' in s['path'] for s in catalog)
assert {s['name'].split(':', 1)[1] for s in catalog} == {Path(p).name for p in manifest['skills']}
result = {'releaseTag': TAG, 'releaseCommit': commit, 'hosts': hosts,
          'freshCatalog': {'count': len(catalog), 'enabled': 44,
                           'names': sorted(s['name'] for s in catalog)}, 'files': files}
(OUT / 'installation.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
print(json.dumps({'releaseTag': TAG, 'releaseCommit': commit, 'hosts': 2,
                  'skillFilesPerHost': len(files), 'freshEnabledSkills': 44, 'status': 'pass'}))
