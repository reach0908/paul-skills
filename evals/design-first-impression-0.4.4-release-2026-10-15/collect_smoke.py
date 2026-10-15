"""Export scoped installation smoke evidence; keep raw host context private."""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
RAW = HERE.parents[1] / '.scratch/first-impression-044-release'
OWNERS = ['better-accessibility', 'better-layout', 'better-writing',
          'better-typography', 'better-colors', 'better-ui']


def sha(value):
    return hashlib.sha256(value).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def events(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.startswith('{')]


def unwrap(value):
    for _ in range(3):
        if not isinstance(value, str):
            break
        try:
            value = json.loads(value)
        except ValueError:
            break
    return value


def sanitize(value, meta):
    return value.replace(meta['plugin_root'], 'PLUGIN').replace(meta['cwd'], 'FIXTURE')


def collect_claude(folder, meta, case):
    rows = events(folder / 'events.jsonl')
    init = next(r for r in rows if r.get('type') == 'system' and r.get('subtype') == 'init')
    result = next((r for r in reversed(rows) if r.get('type') == 'result'), {})
    results = {b.get('tool_use_id'): (i, b) for i, r in enumerate(rows)
               if r.get('type') == 'user' and isinstance(r.get('message', {}).get('content'), list)
               for b in r['message']['content'] if b.get('type') == 'tool_result'}
    calls, launched, line_maps, read_owners = [], [], {}, []
    first_artifact = None
    for i, row in enumerate(rows):
        if row.get('type') != 'assistant':
            continue
        for block in row.get('message', {}).get('content', []):
            if block.get('type') != 'tool_use':
                continue
            result_index, output = results.get(block['id'], (None, {}))
            inp, value = block.get('input', {}), output.get('content', '')
            success = bool(output) and not output.get('is_error')
            entry = {'name': block['name'], 'input': json.loads(sanitize(json.dumps(inp, ensure_ascii=False), meta)),
                     'call_event': i, 'result_event': result_index, 'successful': success,
                     'result_sha256': sha(json.dumps(value, ensure_ascii=False, sort_keys=True).encode())}
            if block['name'] == 'Skill' and success:
                launched.append({'name': inp['skill'].split(':')[-1], 'result_event': result_index})
            if block['name'] == 'Read':
                path = inp.get('file_path', '')
                if path.startswith(meta['cwd'] + '/') and first_artifact is None:
                    first_artifact = i
                text = unwrap(value)
                lines = {int(m[1]): m[2] for line in text.splitlines()
                         if (m := re.match(r'^\s*(\d+)\t(.*)$', line))} if isinstance(text, str) else {}
                line_maps.setdefault(path, {}).update(lines)
                entry['line_numbers'] = sorted(lines)
            calls.append(entry)

    def fully_read(relative):
        path = Path(meta['plugin_root']) / relative
        expected = path.read_text().splitlines()
        actual = line_maps.get(str(path), {})
        return bool(expected) and all(actual.get(i) == line for i, line in enumerate(expected, 1))

    for owner in OWNERS:
        if fully_read(f'skills/design/{owner}/SKILL.md'):
            read_owners.append(owner)
    plugin = next((p for p in init.get('plugins', []) if p.get('name') == 'paul-skills'), {})
    full_response = result.get('result', '')
    if not full_response:
        full_response = '\n\n'.join(b.get('text', '') for r in rows if r.get('type') == 'assistant'
                                     for b in r.get('message', {}).get('content', []) if b.get('type') == 'text')
    receipt = {'completed': meta['exit_code'] == 0 and not meta['timed_out'] and result.get('subtype') == 'success',
               'actual_model': init.get('model'), 'host_version': init.get('claude_code_version'),
               'usage': result.get('usage'), 'model_usage': result.get('modelUsage'),
               'plugin_version': plugin.get('version'), 'plugin_path_matches': plugin.get('path') == meta['plugin_root'],
               'explicit_entry_command_recorded': any('/paul-skills:' + case['skill'] in str(r.get('message', {}).get('content', '')) for r in rows if r.get('type') == 'user'),
               'primary_body_visibility': 'native command expansion receipt; full injected body is not exposed by stream',
               'launched_skills': launched, 'fully_read_owner_files': read_owners,
               'audit_procedure_fully_read': fully_read('skills/design/better-interface/audit-procedure.md'),
               'first_impression_fully_read': fully_read('skills/design/better-layout/first-impression.md'),
               'first_artifact_read_event': first_artifact,
               'all_six_owners_before_artifact': first_artifact is not None and all(any(x['name'] == o and x['result_event'] < first_artifact for x in launched) for o in OWNERS),
               'tool_calls': calls}
    return receipt, sanitize(full_response, meta)


def collect_codex(folder, meta, case):
    rows = events(folder / 'events.jsonl')
    transcript = events(folder / 'transcript.jsonl')
    context = next(r['payload'] for r in transcript if r.get('type') == 'turn_context')
    session = next(r['payload'] for r in transcript if r.get('type') == 'session_meta')
    path = Path(meta['plugin_root']) / f"skills/design/{case['skill']}/SKILL.md"
    body = path.read_text()
    injected = [b.get('text', '') for r in transcript if r.get('type') == 'response_item'
                and r.get('payload', {}).get('role') == 'user'
                for b in r['payload'].get('content', []) if b.get('text', '').startswith('<skill>')]
    exact = any(f'<path>{path}</path>' in value and body in value for value in injected)
    failure = next((r.get('error', {}).get('message', '') for r in rows if r.get('type') == 'turn.failed'), None)
    return {'completed': any(r.get('type') == 'turn.completed' for r in rows) and meta['exit_code'] == 0,
            'actual_model': context.get('model'), 'host_version': session.get('cli_version'),
            'actual_effort': context.get('effort'), 'model_execution': 'blocked_before_response',
            'selected_skill_exact_body_injected': exact, 'selected_skill_sha256': sha(body.encode()),
            'selected_skill_path': 'PLUGIN/' + str(path.relative_to(meta['plugin_root'])),
            'activation_boundary': 'host assembled installed skill in request; model did not execute',
            'failure': failure, 'raw_transcript_sha256': sha((folder / 'transcript.jsonl').read_bytes()),
            'semantic_checks': 'not_run', 'tool_calls': []}, None


def main():
    summaries = []
    for host in ['claude', 'codex']:
        for case in json.loads((HERE / 'cases.json').read_text()):
            folder = RAW / host / case['id']
            identity = f"{host}-{case['id']}"
            if not (folder / 'meta.json').exists():
                receipt = {'host': host, 'case_id': case['id'], 'status': 'not_run',
                           'reason': 'host stopped after two execution failures', 'completed': False}
            else:
                meta = json.loads((folder / 'meta.json').read_text())
                receipt, response = (collect_claude if host == 'claude' else collect_codex)(folder, meta, case)
                receipt.update({k: meta[k] for k in ['host', 'case_id', 'session_id', 'exit_code', 'timed_out',
                    'duration_seconds', 'cost_usd', 'files_before', 'files_after', 'freeze_sha256']})
                receipt.update(status='completed' if receipt['completed'] else 'execution_failed',
                               requested_effort='low', inputs_unchanged=meta['files_before'] == meta['files_after'],
                               raw_events_sha256=sha((folder / 'events.jsonl').read_bytes()))
                if response is not None:
                    target = HERE / 'responses' / (identity + '.md')
                    target.parent.mkdir(exist_ok=True)
                    target.write_text(response + '\n')
                    receipt.update(response=str(target.relative_to(HERE)), response_sha256=sha(target.read_bytes()))
            write(HERE / 'receipts' / (identity + '.json'), receipt)
            summaries.append({k: receipt.get(k) for k in ['host', 'case_id', 'status', 'first_impression_fully_read', 'all_six_owners_before_artifact', 'selected_skill_exact_body_injected', 'cost_usd']})
    print(json.dumps(summaries, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
