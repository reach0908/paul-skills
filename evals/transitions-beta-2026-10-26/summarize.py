#!/usr/bin/env python3
"""Summarize claude plugin eval aggregate JSONs (and their kept traces) into one record.

usage: summarize.py <label>=<aggregate.json> ... > record.json
Tokens are null: aggregate schema 1 reports no token usage.
"""
import json
import re
import sys
from pathlib import Path

SKILL = re.compile(r'(?:[\w-]+:)?([\w-]+)$')


def trace_facts(path):
    facts = {'skills': [], 'edited': [], 'reads': [], 'lastMessage': None, 'traceFound': False}
    p = Path(path) if path else None
    if not p or not p.exists():
        return facts
    facts['traceFound'] = True
    for line in p.read_text().splitlines():
        event = json.loads(line)
        if event.get('type') != 'assistant':
            continue
        for block in event['message'].get('content', []):
            if block.get('type') == 'tool_use':
                name, inp = block['name'], block.get('input', {})
                if name == 'Skill':
                    facts['skills'].append(SKILL.search(inp.get('skill', '')).group(1))
                elif name in ('Edit', 'Write'):
                    facts['edited'].append(Path(inp.get('file_path', '')).name)
                elif name == 'Read':
                    facts['reads'].append(Path(inp.get('file_path', '')).name)
            elif block.get('type') == 'text' and block['text'].strip():
                facts['lastMessage'] = block['text'].strip()
    return facts


record = {'suites': []}
for arg in sys.argv[1:]:
    label, path = arg.split('=', 1)
    agg = json.loads(Path(path).read_text())
    suite = {'label': label, 'claudeVersion': agg['claudeVersion'], 'model': agg['suite']['modelOverride'],
             'ablation': agg['suite']['ablation'], 'costUsd': agg['costUsd'], 'durationSeconds': agg['durationSeconds'],
             'partial': agg['partial'], 'tokens': None, 'runs': []}
    for case in agg['cases']:
        for arm, runs in case['arms'].items():
            for i, run in enumerate(runs):
                facts = trace_facts(run.get('tracePath'))
                suite['runs'].append({
                    'case': case['name'], 'arm': arm, 'run': i, 'error': run['error'],
                    'costUsd': run['costUsd'], 'judgeCostUsd': run['judgeCostUsd'],
                    'durationSeconds': run['durationSeconds'], 'turns': run['turns'],
                    'graders': {g['name']: g['passed'] for g in run['graders']},
                    **facts})
    record['suites'].append(suite)
json.dump(record, sys.stdout, indent=1, ensure_ascii=False)
print()
