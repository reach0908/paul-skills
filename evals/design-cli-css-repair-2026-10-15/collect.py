"""Collect scoped native evidence without exporting private session context."""
from pathlib import Path
import hashlib, importlib.util, json, re

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
RAW = REPO / '.scratch/cli-css-repair-20261015'
spec = importlib.util.spec_from_file_location('release_collector', HERE.parent / 'design-first-impression-0.4.4-release-2026-10-15/collect_smoke.py')
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)
OWNERS = release.OWNERS


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def sha(value):
    return hashlib.sha256(value).hexdigest()


def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.startswith('{')]


def safe(text, meta):
    return text.replace(meta['plugin_root'], 'PLUGIN').replace(meta['cwd'], 'FIXTURE')


def codex(folder, meta, case):
    events = rows(folder / 'events.jsonl')
    trace = rows(folder / 'transcript.jsonl')
    context = next(r['payload'] for r in trace if r.get('type') == 'turn_context')
    session = next(r['payload'] for r in trace if r.get('type') == 'session_meta')
    calls = {r['payload']['call_id']: (i, r['payload']) for i, r in enumerate(trace)
             if r.get('payload', {}).get('type') in {'function_call', 'custom_tool_call'}}
    outputs = [(i, r['payload']) for i, r in enumerate(trace)
               if r.get('payload', {}).get('type') in {'function_call_output', 'custom_tool_call_output'}]
    plugin = Path(meta['plugin_root'])

    def proof(relative):
        path = plugin / relative
        body = path.read_text().strip()
        for index, output in outputs:
            call_index, call = calls.get(output.get('call_id'), (None, {}))
            code = call.get('input', call.get('arguments', ''))
            direct = str(path) in code
            loop = (str(plugin / 'skills/design') + '/${s}/SKILL.md' in code
                    and '"' + path.parent.name + '"' in code)
            if not (direct or loop):
                continue
            value = output.get('output', '')
            texts = [value] if isinstance(value, str) else [b.get('text', '') for b in value if isinstance(b, dict)]
            for text in texts:
                # Native exec may JSON-escape a complete shell output. Partial or
                # truncated copies cannot satisfy either whole-body comparison.
                if body in text or json.dumps(body, ensure_ascii=False)[1:-1] in text:
                    return {'call_event': call_index, 'result_event': index,
                            'full_body_in_model_visible_output': True,
                            'file_sha256': sha(path.read_bytes()), 'output_sha256': sha(text.encode())}
        return None

    primary = plugin / f"skills/design/{case['skill']}/SKILL.md"
    injected = any(f'<path>{primary}</path>' in b.get('text', '') and primary.read_text() in b.get('text', '')
                   for r in trace if r.get('type') == 'response_item' and r.get('payload', {}).get('role') == 'user'
                   for b in r['payload'].get('content', []) if b.get('text', '').startswith('<skill>'))
    first_artifact = next((i for i, call in calls.values()
                           if re.search(r'(?:cat |nl -ba |sed )[^\n]*(?:BRIEF\.md|index\.html|capture\.json)', call.get('input', call.get('arguments', '')))), None)
    owners = {o: p for o in OWNERS if (p := proof(f'skills/design/{o}/SKILL.md'))}
    tool_calls = [{'event': i, 'name': call.get('name'), 'input': safe(call.get('input', call.get('arguments', '')), meta)}
                  for i, call in calls.values()]
    receipt = {'completed': meta['exit_code'] == 0 and any(r['type'] == 'turn.completed' for r in events),
               'actual_model': context.get('model'), 'actual_effort': context.get('effort'),
               'host_version': session.get('cli_version'), 'primary_body_injected': injected,
               'primary_file_sha256': sha(primary.read_bytes()), 'owner_read_proofs': owners,
               'first_impression_read_proof': proof('skills/design/better-layout/first-impression.md'),
               'audit_procedure_read_proof': proof('skills/design/better-interface/audit-procedure.md'),
               'first_artifact_read_event': first_artifact,
               'all_six_owners_before_artifact': first_artifact is not None and len(owners) == 6 and all(p['result_event'] < first_artifact for p in owners.values()),
               'tool_calls': tool_calls,
               'usage': next((r.get('usage') for r in events if r['type'] == 'turn.completed'), None),
               'raw_transcript_sha256': sha((folder / 'transcript.jsonl').read_bytes())}
    return receipt, safe((folder / 'final.md').read_text(), meta)


def collect(group, folder, host, case):
    meta = json.loads((folder / 'meta.json').read_text())
    if 'exit_code' not in meta:
        return None
    meta['plugin_root'] = meta.get('plugin_root', meta.get('bundle'))
    meta['host'] = host
    receipt, response = (codex if host == 'codex' else release.collect_claude)(folder, meta, case)
    identity = (meta['arm'] if 'arm' in meta else host) + '-' + case['id']
    target = HERE / group / 'responses' / (identity + '.md')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(response.rstrip() + '\n')
    receipt.update({k: meta.get(k) for k in ['host', 'arm', 'case_id', 'session_id', 'exit_code', 'timed_out',
                    'duration_seconds', 'cost_usd', 'files_before', 'files_after', 'freeze_sha256']})
    receipt.update(inputs_unchanged=meta['files_before'] == meta['files_after'],
                   raw_events_sha256=sha((folder / 'events.jsonl').read_bytes()),
                   response=str(target.relative_to(HERE)), response_sha256=sha(target.read_bytes()))
    write(HERE / group / 'receipts' / (identity + '.json'), receipt)
    return {'group': group, 'id': identity, 'completed': receipt['completed'],
            'six_owners_before_artifact': receipt.get('all_six_owners_before_artifact'),
            'reference_read': bool(receipt.get('first_impression_read_proof') or receipt.get('first_impression_fully_read'))}


if __name__ == '__main__':
    output = []
    for group, host in [('installed', 'codex'), ('reproduction', 'claude')]:
        for case in json.loads((HERE / group / 'cases.json').read_text()):
            folder = RAW / group / host / case['id']
            if (folder / 'meta.json').exists():
                output.append(collect(group, folder, host, case))
    for case in json.loads((HERE / 'comparison/cases.json').read_text()):
        for arm in ['baseline', 'candidate']:
            folder = RAW / 'comparison' / f"{arm}-{case['id']}"
            if (folder / 'meta.json').exists():
                output.append(collect('comparison', folder, 'claude', dict(case, skill='wireframe')))
    print(json.dumps(output, indent=2))
