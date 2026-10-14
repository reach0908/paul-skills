"""Collect the nine installed entry-point trials without rerunning a model."""
from pathlib import Path
import hashlib
import json
import re

repo = Path(__file__).resolve().parents[2]
raw = repo / '.scratch/design-final-promotion-20261014'
out = Path(__file__).resolve().parent / 'evidence'
home = Path('/private/tmp/paul-design-final-20261014/trial-home')
installed = Path(json.loads((raw / 'trial-add.json').read_text())['installedPath'])
names = ['implicit-ia', 'implicit-flow', 'implicit-wire', 'implicit-build',
         'explicit-state-machine', 'explicit-break', 'explicit-explain-interface', 'explicit-variant', 'explicit-router']
targets = dict(zip(names, ['information-architecture', 'user-flow', 'wireframe', 'build-design',
                         'state-machine', 'break', 'explain-interface', 'variant', 'ask-matt']))
auto = {'information-architecture', 'user-flow', 'wireframe', 'build-design'}
user_only = {'state-machine', 'break', 'explain-interface', 'variant', 'interface-review'}
manifest = json.loads((installed / '.claude-plugin/plugin.json').read_text())
bodies = {Path(p).name: (installed / p / 'SKILL.md').read_text().strip() for p in manifest['skills']}
records = []
for name in names:
    receipt = json.loads((raw / (name + '.receipt.json')).read_text())
    events_file = raw / (name + '.events.jsonl')
    events = [json.loads(line) for line in events_file.read_text().splitlines() if line]
    tid = next(e['thread_id'] for e in events if e.get('type') == 'thread.started')
    commands = [e['item'] for e in events if e.get('type') == 'item.completed'
                and e.get('item', {}).get('type') == 'command_execution']
    loaded = set()
    for c in commands:
        # A later command may exit 1 after a successful full file read.
        output = c.get('aggregated_output', '')
        loaded.update(n for n, body in bodies.items() if body in output)
    rollout = next((home / 'sessions').rglob('*' + tid + '.jsonl'))
    trace = [json.loads(line) for line in rollout.read_text().splitlines() if line]
    context = next(e['payload'] for e in trace if e.get('type') == 'turn_context')
    available, injected = set(), []
    for e in trace:
        if e.get('type') != 'response_item':
            continue
        payload = e.get('payload', {})
        for part in payload.get('content', []):
            text = part.get('text', '') if isinstance(part, dict) else ''
            if payload.get('role') == 'developer' and '### Available skills' in text:
                available.update(re.findall(r'^- (paul-skills:[^:\n]+): ', text, re.M))
            if payload.get('role') == 'user' and text.startswith('<skill>'):
                match = re.search(r'<path>([^<]+)</path>', text)
                if match and str(installed) in match[1]:
                    path = Path(match[1]); skill = path.parent.name
                    assert bodies[skill] in text
                    loaded.add(skill)
                    injected.append({'name': skill, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                                     'contentMatchesInstalledFile': True})
    checks = {'completed': receipt['exitCode'] == 0 and any(e.get('type') == 'turn.completed' for e in events),
              'inputsUnchanged': receipt['before'] == receipt['after'],
              'targetBodyLoaded': targets[name] in loaded,
              'fourAutomaticRolesAvailable': {'paul-skills:' + n for n in auto} <= available,
              'fiveUserOnlyRolesHidden': not ({'paul-skills:' + n for n in user_only} & available)}
    if name.startswith('implicit-'):
        checks['noUserOnlyBodyRead'] = not (loaded & user_only)
        checks['installedTargetPathRead'] = any(str(installed / 'skills/design' / targets[name] / 'SKILL.md') in c['command'] for c in commands)
    else:
        checks['exactTargetBodyInjected'] = any(i['name'] == targets[name] for i in injected)
    final = (raw / (name + '.final.md')).read_text()
    if name == 'explicit-router':
        checks['fourStageRoutePresent'] = all(n in final for n in auto)
        checks['componentWorkbenchNamed'] = 'state-machine' in final
    record = {'case': name, 'target': targets[name], 'threadId': tid, 'model': context['model'],
              'effort': context['effort'], 'installedVersion': manifest['version'], 'checks': checks,
              'loadedSkills': sorted(loaded), 'hostInjectedSkills': injected,
              'automaticallyAvailablePaulSkills': sorted(available), 'receipt': receipt,
              'prompt': (raw / (name + '.prompt.txt')).read_text(), 'final': final,
              'commands': [{'command': c['command'], 'exitCode': c.get('exit_code'),
                            'outputSha256': hashlib.sha256(c.get('aggregated_output', '').encode()).hexdigest()}
                           for c in commands], 'rawTraceSha256': hashlib.sha256(events_file.read_bytes()).hexdigest()}
    (out / (name + '.json')).write_text(json.dumps(record, indent=2, ensure_ascii=False) + '\n')
    records.append(record)
summary = {'cases': len(records), 'passed': sum(all(r['checks'].values()) for r in records),
           'distinctContexts': len({r['threadId'] for r in records}), 'qualityComparisonRepeated': False,
           'actualGlobalInstall': False, 'model': 'gpt-5.6-sol', 'effort': 'xhigh',
           'installedVersion': manifest['version'],
           'failures': {r['case']: [k for k, v in r['checks'].items() if not v] for r in records if not all(r['checks'].values())}}
(out / 'smoke-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
