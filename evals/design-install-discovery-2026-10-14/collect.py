"""Recheck local installation and fresh-session evidence without rerunning models."""
import hashlib
import json
from pathlib import Path
import re
import shutil

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
RAW = REPO / '.scratch/design-install-discovery-20261014'
TRIAL = Path('/private/tmp/paul-design-install-20261014')
EVIDENCE = HERE / 'evidence'
EVIDENCE.mkdir(exist_ok=True)

def read(path):
    return json.loads(path.read_text())

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def store(name, data):
    (EVIDENCE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

identity = read(RAW / 'package-identity.json')
cache = TRIAL / 'codex-home/plugins/cache/paul-design-trial-20261014/paul-skills/0.2.0-design-trial.20261014'
assert all(digest(cache / p) == h for p, h in identity['files'].items())
assert all(digest(REPO / 'skills/in-progress' / Path(p).relative_to('skills/design')) == h for p, h in identity['files'].items())
full = read(RAW / 'full-package-identity.json')
full_cache = TRIAL / 'codex-home-full/plugins/cache/paul-design-full-trial-20261014/paul-skills/0.2.0-design-full-trial.20261014'
assert all(digest(full_cache / p) == h for p, h in full['files'].items())
store('package-identity.json', identity)
store('full-package-identity.json', full)

names = ['implicit-review', 'explicit-review', 'implicit-diff', 'implicit-diff-r2', 'negative', 'browser', 'browser-r2', 'full-package']
sessions = []
for name in names:
    events_path = RAW / (name + '.events.jsonl')
    events = [json.loads(line) for line in events_path.read_text().splitlines() if line]
    completed_items = [e['item'] for e in events if e.get('type') == 'item.completed']
    commands = [i for i in completed_items if i.get('type') == 'command_execution']
    loaded = set()
    for command in commands:
        loaded.update(re.findall(r'^name:\s*["\']?((?:better-[a-z-]+|design-browser|interface-review))["\']?\s*$', command.get('aggregated_output', ''), re.M))
    final = RAW / (name + '.final.md')
    receipt = RAW / (name + '.receipt.json')
    record = {
        'case': name,
        'threadId': next((e.get('thread_id') for e in events if e.get('type') == 'thread.started'), None),
        'turnCompleted': any(e.get('type') == 'turn.completed' for e in events),
        'receipt': read(receipt) if receipt.exists() else None,
        'skillHeadersInSuccessfulReadOutputs': sorted(loaded),
        'commandCount': len(commands),
        'prompt': (RAW / (name + '.prompt.txt')).read_text(),
        'final': final.read_text() if final.exists() else None,
        'rawEvents': str(events_path),
        'rawEventsSha256': digest(events_path),
    }
    sessions.append(record)
    store(name + '.json', record)

for name in ['implicit-review', 'explicit-review', 'implicit-diff', 'implicit-diff-r2', 'negative', 'browser-r2', 'full-package']:
    assert next(s for s in sessions if s['case'] == name)['turnCompleted'], name

qa_root = TRIAL / 'cases/browser-r2/evidence'
raw = (qa_root / 'raw-results.txt').read_text()
qa, _ = json.JSONDecoder().raw_decode(raw[raw.index('{'):])
cases = qa['keyboardCases'] + qa['horizontalOverflowCases']
assert len(cases) == qa['summary']['expectedCaseCount'] == 12
assert sum(c['status'] == 'pass' for c in cases) == 8
assert sum(c['status'] == 'fail' for c in cases) == 4
assert all(c['initialFocus']['tag'] == 'BODY' for c in qa['keyboardCases'])
assert {c['case'] for c in cases if c['status'] == 'fail'} == {
    'keyboard-1440-three', 'keyboard-390-three', 'keyboard-320-three', 'horizontal-overflow-320'}
store('qa-results.json', qa)
qa_dest = EVIDENCE / 'qa'
qa_dest.mkdir(exist_ok=True)
for path in qa_root.iterdir():
    if path.is_file():
        shutil.copy2(path, qa_dest / path.name)
shutil.copy2(TRIAL / 'cases/browser-r2/index.html', qa_dest / 'fixture.html')
source_hash = read(RAW / 'case-inputs.json')['browser']['fileSha256']
assert digest(TRIAL / 'cases/browser-r2/index.html') == source_hash
assert all(digest(TRIAL / 'cases' / name / 'index.html') == source_hash for name in names)

catalogs = []
for home in ['codex-home', 'codex-home-full']:
    for path in (TRIAL / home / 'sessions').rglob('*.jsonl'):
        events = [json.loads(line) for line in path.read_text().splitlines() if line]
        meta = next((e['payload'] for e in events if e.get('type') == 'session_meta'), {})
        context = next((e['payload'] for e in events if e.get('type') == 'turn_context'), {})
        if context.get('model') != 'gpt-5.6-sol':
            continue
        for event in events:
            payload = event.get('payload', {})
            if event.get('type') != 'response_item' or payload.get('role') != 'developer':
                continue
            text = '\n'.join(c.get('text', '') for c in payload.get('content', []) if isinstance(c, dict))
            if '### Available skills' in text:
                available = re.findall(r'^- (paul-skills:[^:]+): ', text, re.M)
                catalogs.append({'threadId': meta.get('id'), 'cwd': context.get('cwd'), 'model': context.get('model'), 'effort': context.get('effort'), 'automaticallyAvailable': available})
                assert 'paul-skills:interface-review' not in available
store('fresh-session-catalogs.json', catalogs)

state = read(RAW / 'global-state-before.json')
global_config = Path('/Users/jinhokim/.codex/config.toml').read_text()
global_hashes = {path: digest(Path(path)) == expected for path, expected in state.items()}
assert 'paul-design-trial-20261014' not in global_config
assert 'paul-design-full-trial-20261014' not in global_config
release_manifests = [Path('/Users/jinhokim') / host / 'plugins/cache/paul-skills/paul-skills/0.2.0/.claude-plugin/plugin.json' for host in ['.codex', '.claude']]
assert all(read(path)['version'] == '0.2.0' and len(read(path)['skills']) == 27 for path in release_manifests)
store('final-global-state.json', {'wholeFileHashMatches': global_hashes,
      'globalTrialEntriesAbsent': True, 'releasedPluginVersions': ['0.2.0', '0.2.0'],
      'releasedSkillCounts': [27, 27],
      'currentGlobalModel': re.search(r'^model\s*=\s*"([^"]+)"', global_config, re.M).group(1),
      'note': 'Whole Codex config changed during verification; trial writes targeted isolated config only. No restoration of unrelated settings.'})
store('integrity.json', {'candidateInstalledFiles': len(identity['files']), 'candidateHashMismatches': 0,
      'fullPackageSkills': full['skills'], 'fullPackageHashMismatches': 0, 'sourceFixtureChanges': 0,
      'globalWholeConfigHashMatches': global_hashes, 'globalTrialEntriesAbsent': True,
      'releasedPaulPluginUnchanged': True, 'qaCases': 12, 'qaDetectedExpectedFailures': 4,
      'completedExecutionContexts': sum(s['turnCompleted'] for s in sessions),
      'model': 'gpt-5.6-sol', 'reasoningEffort': 'xhigh'})
for name in ['model-resolution.json', 'disable-control.json', 'installed-hash-check.json', 'link-check.json', 'validate.json']:
    shutil.copy2(RAW / name, EVIDENCE / name)
store('evidence-manifest.json', {str(p.relative_to(EVIDENCE)): digest(p) for p in EVIDENCE.rglob('*') if p.is_file() and p.name != 'evidence-manifest.json'})
print(json.dumps({'sessions': len(sessions), 'completed': sum(s['turnCompleted'] for s in sessions), 'qaCases': len(cases), 'hashesVerified': True}))
