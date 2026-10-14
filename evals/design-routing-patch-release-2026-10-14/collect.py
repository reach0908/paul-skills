#!/usr/bin/env python3
"""Collect host evidence, never award an invocation for an assistant's claim."""
import json
from pathlib import Path
import re
import subprocess

from run_trials import CACHE, BUNDLE, HERE, RAW, REPO, read_events, digest

CONFIG = json.loads((HERE / 'cases.json').read_text())
CASES = CONFIG['cases']
USER_ONLY = set(CONFIG['user_only'])
NAMES = {p.name for p in (REPO / 'skills/design').iterdir() if (p / 'SKILL.md').exists()}
AUTO = NAMES - USER_ONLY
OUT = HERE / 'claude'


def public_json(value):
    # Preserve model text while avoiding literal em dashes in repository prose.
    return json.dumps(value, ensure_ascii=False, indent=2).replace("\N{EM DASH}", r"\u2014") + '\n'


def texts(event):
    content = event.get('message', {}).get('content', [])
    if isinstance(content, str):
        return [content]
    return [block['text'] for block in content if block.get('type') == 'text']


def body_of(source):
    return source.split('---', 2)[2].strip() if source.startswith('---\n') else source.strip()


def loaded_body(text, source, directory=None):
    """Require a host expansion prefix and the entire exact body."""
    if not text.startswith('Base directory for this skill: '):
        return False
    if directory is not None and text.split('\n', 1)[0] != f'Base directory for this skill: {directory}':
        return False
    _, separator, rendered = text.partition('\n\n')
    body = body_of(source)
    if not separator or not rendered.startswith(body):
        return False
    tail = rendered[len(body):].strip()
    return not tail or tail.startswith('ARGUMENTS:')


def short_name(name):
    return name.removeprefix('paul-skills:')


def redact(value, cwd):
    if isinstance(value, str):
        return value.replace(cwd, '$TRIAL').replace(str(REPO), '$REPO').replace(str(Path.home()), '$HOME')
    if isinstance(value, dict):
        return {k: redact(v, cwd) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(v, cwd) for v in value]
    return value


def collect_case(case):
    case_id = case['id']
    meta_path = RAW / f'{case_id}.meta.json'
    transcript_path = RAW / f'{case_id}.transcript.jsonl'
    if not meta_path.exists() or not transcript_path.exists():
        return None
    meta = json.loads(meta_path.read_text())
    cache = Path(meta.get('plugin_root', str(CACHE)))
    if 'exit_code' not in meta:
        return None
    stream_path = RAW / f'{case_id}.jsonl'
    stderr_path = RAW / f'{case_id}.stderr'
    stream = read_events(stream_path)
    transcript = read_events(transcript_path)
    init = next((e for e in stream if e.get('type') == 'system' and e.get('subtype') == 'init'), {})
    result = next((e for e in reversed(stream) if e.get('type') == 'result'), {})
    initial = next((e for e in transcript if e.get('attachment', {}).get('type') == 'skill_listing'
                    and e['attachment'].get('isInitial')), {})
    listings = initial.get('attachment', {})
    visible = sorted(short_name(n) for n in listings.get('names', []) if n.startswith('paul-skills:') and short_name(n) in NAMES)
    commands = sorted(short_name(n) for n in init.get('slash_commands', []) if n.startswith('paul-skills:') and short_name(n) in NAMES)
    sources = {n: (cache / 'skills/design' / n / 'SKILL.md').read_text() for n in NAMES}
    bodies = []
    for event in transcript:
        if event.get('type') != 'user':
            continue
        for text in texts(event):
            for name, source in sources.items():
                if loaded_body(text, source, cache / 'skills/design' / name):
                    bodies.append({'name': name, 'event_uuid': event.get('uuid'),
                                   'file_sha256': digest(source.encode()),
                                   'body_sha256': digest(body_of(source).encode()),
                                   'host_message_sha256': digest(text.encode()),
                                   'full_body_equal': True})
    tool_results = {}
    for event in transcript:
        if event.get('type') != 'user':
            continue
        content = event.get('message', {}).get('content', [])
        if isinstance(content, list):
            for block in content:
                if block.get('type') == 'tool_result':
                    tool_results[block['tool_use_id']] = block
    calls = []
    efforts = set()
    for event in transcript:
        if event.get('type') != 'assistant':
            continue
        if event.get('effort'):
            efforts.add(event['effort'])
        for block in event.get('message', {}).get('content', []):
            if block.get('type') != 'tool_use':
                continue
            receipt = tool_results.get(block['id'])
            calls.append({'name': block['name'], 'input': redact(block['input'], meta['cwd']),
                          'tool_use_id': block['id'], 'result_present': receipt is not None,
                          'is_error': receipt.get('is_error', False) if receipt else None,
                          'result_sha256': digest(json.dumps(receipt, sort_keys=True, ensure_ascii=False).encode()) if receipt else None})
    loaded = {b['name'] for b in bodies}
    invoked = {short_name(c['input'].get('skill', '')) for c in calls
               if c['name'] == 'Skill' and c['result_present'] and not c['is_error']}
    attempted = set()
    for call in calls:
        if call['name'] == 'Skill':
            attempted.add(short_name(call['input'].get('skill', '')))
        elif call['name'] in {'Read', 'Grep', 'Glob'}:
            value = json.dumps(call['input'])
            attempted.update(n for n in USER_ONLY if re.search(r'(?:^|[/" ])'+re.escape(n)+r'(?:/|["*])', value))
    read_bodies = set()
    for receipt in tool_results.values():
        content = receipt.get('content', '')
        if not isinstance(content, str):
            content = '\n'.join(b.get('text', '') for b in content if isinstance(b, dict))
        content = re.sub(r'^\s*\d+\s*[→\t]\s?', '', content, flags=re.MULTILINE)
        read_bodies.update(n for n in USER_ONLY if body_of(sources[n]) in content)
    hidden_loads = sorted((loaded | attempted | read_bodies) & USER_ONLY)
    complete = (meta.get('exit_code') == 0 and not meta.get('timed_out')
                and result.get('subtype') == 'success' and not result.get('is_error')
                and bool(result.get('result')))
    final = result.get('result', '')
    checks = {
        'model_completed': complete,
        'host_session_matches_request': init.get('session_id') == result.get('session_id') == meta['session_id'],
        'automatic_catalog_exact_12': set(visible) == AUTO and len(visible) == len(AUTO),
        'direct_catalog_all_17': set(commands) == NAMES and len(commands) == len(NAMES),
        'correct_plugin_source': any(p.get('name') == 'paul-skills' and p.get('version') == '0.4.1'
                           and p.get('path') == str(cache) for p in init.get('plugins', [])),
        'inputs_unchanged': meta.get('files_before') == meta.get('files_after'),
        'no_permission_denials': not result.get('permission_denials'),
        'no_failed_tools': all(c['result_present'] and not c['is_error'] for c in calls),
    }
    manual_path = HERE / 'manual-review.json'
    manual = json.loads(manual_path.read_text()) if manual_path.exists() else {}
    checks['semantic_review_pass'] = manual.get('cases', {}).get(case_id, {}).get('pass') is True
    checks['actual_global_no_override'] = '--plugin-dir' not in meta['command']
    protocol2 = meta['protocol_sha256'] == digest((HERE / 'PROTOCOL.md').read_bytes())
    if protocol2:
        checks['neutral_working_directory'] = bool(re.fullmatch(r'case_\d{3}', Path(meta['cwd']).name))
    if case['mode'] in {'explicit', 'handoff'}:
        checks['target_body_equal'] = case['expected'] in loaded
        checks['no_other_user_only_loads'] = not (set(hidden_loads) - {case['expected']})
    elif case['mode'] == 'implicit':
        checks['expected_skill_invoked_and_loaded'] = case['expected'] in invoked & loaded
        checks['no_user_only_loads_or_attempts'] = not hidden_loads
    else:
        checks['no_user_only_loads_or_attempts'] = not hidden_loads
        if case['forbidden'] in {'interface-review', 'state-machine'}:
            checks['expected_owner'] = case['expected'] in (loaded if case.get('entry') == 'explicit' else invoked & loaded)
        if case['forbidden'] == 'interface-review':
            target = case.get('target', 'working')
            checks['explicit_handoff'] = ('/paul-skills:interface-review' + (' ' + target if target else '')) in final
            if not target:
                primary = re.search(r'/paul-skills:interface-review([^`\n]*)', final)
                checks['no_invented_target'] = primary is not None and not primary.group(1).strip()
            checks['no_domain_calls'] = not (invoked & {'better-accessibility', 'better-layout', 'better-writing', 'better-typography', 'better-colors', 'better-ui'})
            checks['no_file_inspection'] = not any(c['name'] in {'Read', 'Grep', 'Glob', 'Bash'} for c in calls)
    if case['id'].removeprefix('followup-') == 'repair-current-audit':
        review_path = HERE / 'manual-review.json'
        reviews = json.loads(review_path.read_text()).get('cases', {}) if review_path.exists() else {}
        checks['no_change_review_redirect'] = reviews.get(case['id'], {}).get('no_change_review_redirect') is True
    if case['mode'] == 'handoff':
        owners = {'better-interface', 'better-accessibility', 'better-layout', 'better-writing', 'better-typography', 'better-colors', 'better-ui'}
        checks['authorized_owners_loaded'] = owners <= invoked & loaded
        checks['real_git_diff'] = any(c['name'] == 'Bash' and c['result_present'] and not c['is_error'] and 'git diff' in c['input'].get('command', '') for c in calls)
        checks['classified_regression'] = 'Regression' in final and 'aria-label' in final
    return {
        'arm': case.get('arm', 'candidate'), 'fixture': case.get('fixture'),
        'bundle_manifest_sha256': meta.get('bundle_manifest_sha256'),
        'schema_version': 1, 'case_id': case_id, 'mode': case['mode'],
        'protocol_version': 1,
        'trial_directory_name': Path(meta['cwd']).name,
        'expected': case.get('expected'), 'prompt': case['prompt'],
        'session_id': meta['session_id'], 'started_at': meta['started_at'],
        'host_init_session_id': init.get('session_id'), 'host_result_session_id': result.get('session_id'),
        'host_version': init.get('claude_code_version'), 'model': init.get('model'),
        'available_tools': init.get('tools'),
        'mcp_servers': init.get('mcp_servers'),
        'effort_observed': sorted(efforts), 'permission_mode': init.get('permissionMode'),
        'plugin': [redact(p, meta['cwd']) for p in init.get('plugins', []) if p.get('name') == 'paul-skills'],
        'automatic_design_catalog': visible, 'direct_design_catalog': commands,
        'automatic_catalog_event_uuid': initial.get('uuid'),
        'automatic_catalog_sha256': digest(json.dumps(listings, sort_keys=True).encode()),
        'full_body_loads': bodies, 'tool_calls': calls, 'user_only_loads_or_attempts': hidden_loads,
        'user_only_bodies_in_file_results': sorted(read_bodies),
        'final_response': redact(final, meta['cwd']), 'checks': checks,
        'pass': all(checks.values()), 'duration_seconds': meta['duration_seconds'],
        'duration_api_ms': result.get('duration_api_ms'), 'usage': result.get('usage'),
        'model_usage': result.get('modelUsage'), 'reported_cost_usd': result.get('total_cost_usd'),
        'cost_basis': 'host-reported list estimate; actual invoice not available',
        'actual_billed_usd': None,
        'permission_denials': redact(result.get('permission_denials', []), meta['cwd']),
        'input_before': meta['files_before'], 'input_after': meta['files_after'],
        'exit_code': meta['exit_code'], 'result_subtype': result.get('subtype'),
        'api_error_status': result.get('api_error_status'),
        'stop_reason': result.get('stop_reason'), 'num_turns': result.get('num_turns'),
        'protocol_sha256': meta['protocol_sha256'], 'cases_sha256': meta['cases_sha256'],
        'stream_sha256': digest(stream_path.read_bytes()),
        'transcript_sha256': digest(transcript_path.read_bytes()),
        'stderr_sha256': digest(stderr_path.read_bytes()) if stderr_path.exists() else None,
        'stderr_bytes': stderr_path.stat().st_size if stderr_path.exists() else None,
    }



def main():
    OUT.mkdir(exist_ok=True)
    rows = []
    for case in CASES:
        row = collect_case(case)
        if row:
            (OUT / (case['id'] + '.json')).write_text(public_json(row))
            rows.append(row)
    summary = {
        'planned': len(CASES), 'completed': len(rows),
        'by_arm': {arm: {'completed': sum(r['arm'] == arm for r in rows),
                        'passed': sum(r['arm'] == arm and r['pass'] for r in rows)} for arm in ['installed']},
        'by_mode_installed': {mode: {'completed': sum(r['arm'] == 'installed' and r['mode'] == mode for r in rows),
                                   'passed': sum(r['arm'] == 'installed' and r['mode'] == mode and r['pass'] for r in rows)} for mode in ['explicit','implicit','boundary','handoff']},
        'failures': [{'case_id':r['case_id'], 'failed_checks':[k for k,v in r['checks'].items() if not v]} for r in rows if not r['pass']],
        'reported_cost_usd':sum(r['reported_cost_usd'] or 0 for r in rows),
        'actual_billed_usd':None,
        'models':sorted({r['model'] for r in rows}),
        'efforts':sorted({e for r in rows for e in r['effort_observed']})}
    (OUT / 'summary.json').write_text(public_json(summary))
    print(public_json(summary))

if __name__ == '__main__':
    main()
