"""Collect actual fresh-session traces and check routing, installation and source identity."""
from pathlib import Path
import hashlib
import json
import re
import shutil

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
RAW = REPO / '.scratch/design-routing-repair-20261014'
EVIDENCE = HERE / 'evidence'
DOMAINS = {'better-accessibility', 'better-layout', 'better-writing', 'better-typography', 'better-colors', 'better-ui'}


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def store(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


all_records = []
for attempt in [1, 2]:
    raw = RAW if attempt == 1 else RAW / 'attempt-2'
    trial = Path('/private/tmp/paul-design-routing-20261014' + ('' if attempt == 1 else '-r2'))
    evidence = EVIDENCE / ('attempt-' + str(attempt))
    identity = read(raw / 'package-identity.json')
    cache = trial / 'codex-home/plugins/cache/paul-design-routing-trial-20261014/paul-skills/0.2.0-routing-trial.20261014'
    assert all(digest(cache / row['installed']) == row['sha256'] for row in identity)
    if attempt == 2:
        assert all(digest(REPO / row['source']) == row['sha256'] for row in identity)
    inputs = read(raw / 'case-inputs.json')
    catalog = read(raw / 'catalog-selected.json')
    assert len(catalog) == 36 and all(s['enabled'] for s in catalog)
    prior_inputs = read(REPO / '.scratch/design-install-discovery-20261014/case-inputs.json')
    for value in inputs.values():
        if value['priorCase']:
            prior_input = prior_inputs[value['priorCase']]
            assert value['promptSha256'] == prior_input['promptSha256']
            assert value['fileSha256'] == prior_input['fileSha256']
    catalogs = {}
    for path in (trial / 'codex-home/sessions').rglob('*.jsonl'):
        entries = [json.loads(line) for line in path.read_text().splitlines() if line]
        meta = next(e['payload'] for e in entries if e.get('type') == 'session_meta')
        context = next(e['payload'] for e in entries if e.get('type') == 'turn_context')
        for event in entries:
            p = event.get('payload', {})
            if event.get('type') != 'response_item' or p.get('role') != 'developer':
                continue
            text = '\n'.join(c.get('text', '') for c in p.get('content', []) if isinstance(c, dict))
            if '### Available skills' in text:
                available = re.findall(r'^- (paul-skills:[^:]+): ', text, re.M)
                catalogs[meta['id']] = {'model': context['model'], 'effort': context['effort'], 'automaticallyAvailable': available}
    records = []
    for name, input_record in inputs.items():
        events_path = raw / (name + '.events.jsonl')
        events = [json.loads(line) for line in events_path.read_text().splitlines() if line]
        receipt = read(raw / (name + '.receipt.json'))
        assert receipt['exitCode'] == 0
        assert any(e.get('type') == 'turn.completed' for e in events)
        thread_id = next(e['thread_id'] for e in events if e.get('type') == 'thread.started')
        commands = [e['item'] for e in events if e.get('type') == 'item.completed' and e['item'].get('type') == 'command_execution']
        loaded = set()
        for command in commands:
            if command.get('exit_code') == 0:
                loaded.update(re.findall(r'^name:\s*["\']?((?:better-[a-z-]+|design-browser|interface-review))["\']?\s*$', command.get('aggregated_output', ''), re.M))
        final = (raw / (name + '.final.md')).read_text()
        assert digest(trial / 'cases' / name / 'index.html') == input_record['fileSha256']
        assert digest(raw / (name + '.prompt.txt')) == input_record['promptSha256']
        cat = catalogs[thread_id]
        assert cat['model'] == 'gpt-5.6-sol' and cat['effort'] == 'xhigh'
        assert 'paul-skills:interface-review' not in cat['automaticallyAvailable']
        assert all('paul-skills:' + s in cat['automaticallyAvailable'] for s in DOMAINS | {'better-interface', 'design-browser'})
        checks = {'sourceUnchanged': True, 'freshSessionCompleted': True, 'userOnlySkillHidden': True}
        if name.startswith('implicit-diff') or name == 'implicit-staged':
            target = 'staged' if name == 'implicit-staged' else 'working'
            checks['correctInvocationTarget'] = '$paul-skills:interface-review ' + target in final
            checks['onlyRoutingSkillRead'] = loaded == {'better-interface'}
            checks['noDiffOrSourceInspection'] = len(commands) == 1 and 'better-interface/SKILL.md' in commands[0]['command'] and not re.search(r'\bgit\b|index\.html', commands[0]['command'])
            checks['noReviewVerdict'] = not re.search(r'\b(?:Approve|Block|Needs improvement|HIGH)\b', final)
        elif name.startswith('implicit-review') or name == 'explicit-review':
            checks['sixDomainsLoaded'] = DOMAINS | {'better-interface'} <= loaded
            checks['keyboardDefectRetained'] = 'tabindex' in final and 'HIGH' in final and 'Block' in final
            checks['limitsDeclared'] = '검증' in final or 'verified' in final.lower()
            if name == 'explicit-review':
                checks['explicitChangeSkillLoaded'] = 'interface-review' in loaded
                checks['changeAndExistingSeparated'] = 'Regression' in final and ('Pre-existing' in final or '기존 문제' in final) and 'min-width' in final
            else:
                # Supplementary comparison against valid findings in the prior screen report.
                checks['widthFindingRetained'] = 'min-width' in final and '320' in final
                checks['fontPreferenceFindingRetained'] = '1rem' in final
                checks['duplicateDetailFindingRetained'] = bool(re.search('복사|복제|되풀이|요약', final))
        else:
            checks['noToolUse'] = not commands
            checks['correctArithmetic'] = final.strip() == '102'
        record = {'attempt': attempt, 'case': name, 'threadId': thread_id, 'receipt': receipt,
                  'prompt': (raw / (name + '.prompt.txt')).read_text(), 'input': input_record,
                  'loadedSkillHeaders': sorted(loaded), 'catalog': cat, 'final': final, 'checks': checks,
                  'status': 'pass' if all(checks.values()) else 'fail',
                  'commands': [{'command': c['command'], 'exitCode': c.get('exit_code'), 'outputSha256': hashlib.sha256(c.get('aggregated_output', '').encode()).hexdigest()} for c in commands],
                  'rawEvents': str(events_path), 'rawEventsSha256': digest(events_path)}
        store(evidence / (name + '.json'), record)
        records.append(record)
    for name in ['package-identity.json', 'catalog-selected.json', 'plugin-add.json', 'plugin-list.json', 'plugin-validate.json', 'case-inputs.json']:
        shutil.copy2(raw / name, evidence / name)
    store(evidence / 'summary.json', {'skills': 36, 'files': len(identity), 'caseCount': len(records), 'passed': sum(r['status'] == 'pass' for r in records), 'allPackageHashesMatch': True})
    all_records.extend(records)

# Pin the exact edited files, including the failed first candidate.
for name in ['better-interface', 'interface-review']:
    shutil.copy2(RAW / 'before' / (name + '.md'), EVIDENCE / (name + '-before.md'))
    for attempt, suffix in [(1, ''), (2, '-r2')]:
        source = Path('/private/tmp/paul-design-routing-20261014' + suffix) / 'marketplace/plugin/skills/design' / name / 'SKILL.md'
        shutil.copy2(source, EVIDENCE / f'{name}-attempt-{attempt}.md')
    before = (RAW / 'before' / (name + '.md')).read_text()
    after = (REPO / 'skills/in-progress' / name / 'SKILL.md').read_text()
    if name == 'better-interface':
        assert before.split('### 3. Recon before judgment', 1)[1] == after.split('### 3. Recon before judgment', 1)[1]
    else:
        assert before.split('### 1. Resolve the change scope first', 1)[1].split('### 7. Hand the review', 1)[0] == after.split('### 1. Resolve the change scope first', 1)[1].split('### 7. Hand the review', 1)[0]
        assert before.split('### 8. Never mutate the working tree', 1)[1] == after.split('### 8. Never mutate the working tree', 1)[1]

old_identity = read(REPO / '.scratch/design-install-discovery-20261014/package-identity.json')['files']
final_identity = read(RAW / 'attempt-2/package-identity.json')
changed_candidates = [row['installed'] for row in final_identity if row['installed'].startswith('skills/design/') and old_identity.get(row['installed']) != row['sha256']]
assert changed_candidates == ['skills/design/better-interface/SKILL.md', 'skills/design/interface-review/SKILL.md'], changed_candidates
final_records = [r for r in all_records if r['attempt'] == 2]
assert len({r['threadId'] for r in all_records}) == len(all_records)
final_passed = sum(r['status'] == 'pass' for r in final_records)
store(EVIDENCE / 'integrity.json', {'finalCases': len(final_records), 'finalPassed': final_passed, 'attempts': 2, 'sessions': len(all_records), 'fullPluginSkills': 36, 'changedCandidateFiles': changed_candidates, 'reviewRuleSectionsUnchanged': True, 'productSourcesUnchanged': True})
store(EVIDENCE / 'evidence-manifest.json', {str(p.relative_to(EVIDENCE)): digest(p) for p in EVIDENCE.rglob('*') if p.is_file() and p.name != 'evidence-manifest.json'})
print(json.dumps({'attempts': 2, 'sessions': len(all_records), 'finalPassed': final_passed, 'finalCases': len(final_records), 'firstAttemptFailures': [r['case'] for r in all_records if r['attempt'] == 1 and r['status'] != 'pass']}))
