"""Build an isolated full-plugin trial without changing the daily installation."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess

REPO = Path(__file__).resolve().parents[2]

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from skill_paths import skill_directory
ATTEMPT = os.environ.get('PAUL_TRIAL_ATTEMPT', '2')
SUFFIX = '' if ATTEMPT == '1' else '-r' + ATTEMPT
ROOT = Path('/private/tmp/paul-design-routing-20261014' + SUFFIX)
RAW = REPO / '.scratch/design-routing-repair-20261014'
if ATTEMPT != '1':
    RAW /= 'attempt-' + ATTEMPT
PRIOR = REPO / '.scratch/design-install-discovery-20261014'
CANDIDATES = ['better-interface', 'better-accessibility', 'better-layout', 'better-writing', 'better-typography', 'better-colors', 'better-ui', 'design-browser', 'interface-review']
assert not ROOT.exists(), 'Preserve an existing trial; use a new root for a new attempt.'
ROOT.mkdir()
RAW.mkdir(parents=True, exist_ok=True)
plugin = ROOT / 'marketplace/plugin'
(plugin / '.claude-plugin').mkdir(parents=True)
manifest = json.loads((REPO / '.claude-plugin/plugin.json').read_text())
identity = []
sources = {p.removeprefix('./'): p.removeprefix('./') for p in manifest['skills']}
for name in CANDIDATES:
    sources[f'skills/design/{name}'] = str(skill_directory(REPO, name).relative_to(REPO))
for destination, source in sources.items():
    shutil.copytree(REPO / source, plugin / destination)
    for f in sorted((plugin / destination).rglob('*')):
        if f.is_file():
            relative = f.relative_to(plugin / destination)
            identity.append({'source': str(Path(source) / relative), 'installed': str(f.relative_to(plugin)), 'sha256': hashlib.sha256(f.read_bytes()).hexdigest()})
manifest['version'] = '0.2.0-routing-trial.20261014'
manifest['skills'] = ['./' + path for path in sources]
(plugin / '.claude-plugin/plugin.json').write_text(json.dumps(manifest, indent=2) + '\n')
market = ROOT / 'marketplace/.claude-plugin'
market.mkdir()
(market / 'marketplace.json').write_text(json.dumps({'name': 'paul-design-routing-trial-20261014', 'owner': {'name': 'Paul Kim'}, 'plugins': [{'name': 'paul-skills', 'source': './plugin', 'category': 'design'}]}, indent=2) + '\n')
(RAW / 'package-identity.json').write_text(json.dumps(identity, indent=2) + '\n')
harness = ROOT / 'codex-home'
harness.mkdir()
# Refer to existing login only for this authorized model test. Never copy credentials into evidence.
(harness / 'auth.json').symlink_to(Path('/Users/jinhokim/.codex/auth.json'))
config = 'model = "gpt-5.6-sol"\nmodel_reasoning_effort = "xhigh"\n'
cases = {
    'implicit-diff-a': 'implicit-diff',
    'implicit-diff-b': 'implicit-diff',
    'implicit-review': 'implicit-review',
    'explicit-review': 'explicit-review',
    'implicit-staged': 'implicit-diff',
    'negative': 'negative',
}
if ATTEMPT != '1':
    cases['implicit-review-repeat'] = 'implicit-review'
inputs = {}
for name, prior in cases.items():
    workspace = ROOT / 'cases' / name
    shutil.copytree(Path('/private/tmp/paul-design-install-20261014/cases') / prior, workspace)
    prompt = (PRIOR / (prior + '.prompt.txt')).read_text()
    if name == 'implicit-staged':
        subprocess.run(['git', 'add', 'index.html'], cwd=workspace, check=True)
        prompt = '스테이징한 UI 변경에서 이번 변경으로 새로 생긴 문제만 검토해 주세요. 소스만 보고 파일 수정이나 브라우저 실행은 하지 마세요.\n'
    (RAW / (name + '.prompt.txt')).write_text(prompt)
    config += f'\n[projects."{workspace}"]\ntrust_level = "trusted"\n'
    inputs[name] = {'priorCase': prior if name != 'implicit-staged' else None, 'workspace': str(workspace), 'promptSha256': hashlib.sha256(prompt.encode()).hexdigest(), 'fileSha256': hashlib.sha256((workspace / 'index.html').read_bytes()).hexdigest()}
(harness / 'config.toml').write_text(config)
(RAW / 'case-inputs.json').write_text(json.dumps(inputs, indent=2) + '\n')
env = dict(os.environ, CODEX_HOME=str(harness))
for name, cmd in [
    ('marketplace-add', ['codex', 'plugin', 'marketplace', 'add', str(ROOT / 'marketplace'), '--json']),
    ('plugin-add', ['codex', 'plugin', 'add', 'paul-skills@paul-design-routing-trial-20261014', '--json']),
    ('plugin-list', ['codex', 'plugin', 'list', '--json']),
    ('plugin-validate', ['claude', 'plugin', 'validate', str(plugin), '--strict']),
]:
    p = subprocess.run(cmd, env=env, text=True, capture_output=True)
    (RAW / (name + '.json')).write_text(json.dumps({'command': cmd, 'exitCode': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr}, indent=2) + '\n')
    assert p.returncode == 0, name
print(json.dumps({'root': str(ROOT), 'skills': len(manifest['skills']), 'files': len(identity), 'cases': list(cases)}))
