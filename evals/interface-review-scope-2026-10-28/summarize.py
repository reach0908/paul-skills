#!/usr/bin/env python3
"""Summarize claude plugin eval aggregate JSONs (and their kept traces) into one record.

usage: summarize.py <label>=<aggregate.json> ... > record.json
Trace paths in the aggregate are relative to its directory. Skills come from the trace's Skill tool_use blocks, paired with their tool_result so a failed
load is visible (loaded=false). SKILL.md reads through Read are listed separately. Aggregate
schema 1 reports no token usage, so tokens come from the trace's result event and stay null
when the trace or its usage is missing. Missing telemetry is null, never zero.
"""
import json
import re
import sys
from pathlib import Path

SKILL = re.compile(r'(?:[\w-]+:)?([\w-]+)$')
OWNERS = ['better-accessibility', 'better-layout', 'better-writing', 'better-typography', 'better-colors', 'better-ui']


def trace_facts(path):
    facts = {'traceFound': False, 'skillCalls': [], 'skillMdReads': [], 'referenceReads': [], 'bashCommands': 0,
             'ownersLoaded': None, 'lastMessage': None, 'tokens': None, 'traceCostUsd': None, 'costBasis': None, 'model': None}
    p = Path(path) if path else None
    if not p or not p.exists():
        return facts
    facts['traceFound'] = True
    pending = {}
    for line in p.read_text().splitlines():
        event = json.loads(line)
        if event.get('type') == 'result':
            usage = event.get('usage') or {}
            if usage:
                facts['tokens'] = {'input': usage.get('input_tokens'), 'output': usage.get('output_tokens'),
                                   'cacheRead': usage.get('cache_read_input_tokens'),
                                   'cacheCreation': usage.get('cache_creation_input_tokens'),
                                   'thinking': (usage.get('output_tokens_details') or {}).get('thinking_tokens')}
            facts['traceCostUsd'] = event.get('total_cost_usd')
            models = event.get('modelUsage') or {}
            if models:
                facts['model'] = sorted(models)
                facts['costBasis'] = next(iter(models.values()), {}).get('costBasis')
        if event.get('type') == 'user':
            for block in (event.get('message') or {}).get('content') or []:
                if isinstance(block, dict) and block.get('type') == 'tool_result' and block.get('tool_use_id') in pending:
                    pending.pop(block['tool_use_id'])['loaded'] = not block.get('is_error', False)
        if event.get('type') != 'assistant':
            continue
        for block in event['message'].get('content', []):
            if block.get('type') == 'tool_use':
                name, inp = block['name'], block.get('input', {})
                if name == 'Skill':
                    call = {'skill': SKILL.search(inp.get('skill', '')).group(1), 'loaded': None}
                    facts['skillCalls'].append(call)
                    pending[block['id']] = call
                elif name == 'Read':
                    fp = inp.get('file_path', '')
                    parts = Path(fp).parts
                    rel = '/'.join(parts[-2:])
                    (facts['skillMdReads'] if fp.endswith('SKILL.md') else facts['referenceReads']).append(rel)
                elif name == 'Bash':
                    facts['bashCommands'] += 1
            elif block.get('type') == 'text' and block['text'].strip():
                facts['lastMessage'] = block['text'].strip()
    loaded = {c['skill'] for c in facts['skillCalls'] if c['loaded']}
    loaded |= {r.split('/')[0] for r in facts['skillMdReads']}
    facts['ownersLoaded'] = [o for o in OWNERS if o in loaded]
    return facts


record = {'suites': []}
for arg in sys.argv[1:]:
    label, path = arg.split('=', 1)
    agg = json.loads(Path(path).read_text())
    suite = {'label': label, 'startedAt': agg['startedAt'], 'claudeVersion': agg['claudeVersion'],
             'model': agg['suite'].get('modelOverride'), 'ablation': agg['suite'].get('ablation'),
             'costUsd': agg.get('costUsd'), 'durationSeconds': agg.get('durationSeconds'),
             'partial': agg.get('partial'), 'runs': []}
    for case in agg['cases']:
        for arm, runs in case['arms'].items():
            for i, run in enumerate(runs):
                suite['runs'].append({
                    'case': case['name'], 'arm': arm, 'run': i, 'startedAt': run.get('startedAt'),
                    'error': run.get('error'), 'costUsd': run.get('costUsd'), 'judgeCostUsd': run.get('judgeCostUsd'),
                    'durationSeconds': run.get('durationSeconds'), 'turns': run.get('turns'),
                    'graders': {g['name']: g['passed'] for g in run.get('graders', [])},
                    **trace_facts(Path(path).parent / run['tracePath'] if run.get('tracePath') else None)})
    record['suites'].append(suite)
json.dump(record, sys.stdout, indent=1, ensure_ascii=False)
print()
