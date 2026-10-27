#!/usr/bin/env python3
"""Re-apply the graders amended after the main run (see PROTOCOL.md amendment) to kept traces.

usage: regrade.py <aggregate.json>   (prints JSON: {case/run: {grader: passed}})
Uses the current cases/*/case.yaml patterns with JavaScript regex semantics through
evals/claude-native/tools/regex_eval.mjs. last_message is the trace's result event text;
tool_used inputs are the JSON-encoded tool input, as the runner matches them.
"""
import json
import subprocess
import sys
from pathlib import Path

AMENDED = {'S3-reflow-finding', 'RO-no-checkout-mutation'}
here = Path(__file__).parent
regex_eval = here.parents[0] / 'claude-native/tools/regex_eval.mjs'
agg_path = Path(sys.argv[1])
agg = json.loads(agg_path.read_text())


def js(items):
    out = subprocess.run(['node', str(regex_eval)], input=json.dumps(items), capture_output=True, text=True, check=True)
    return {r['id']: r for r in json.loads(out.stdout)}


result = {}
for case in agg['cases']:
    graders = [g for g in json.loads((here / 'cases' / case['name'] / 'case.yaml').read_text())['graders'] if g['name'] in AMENDED]
    for runs in case['arms'].values():
        for i, run in enumerate(runs):
            trace = agg_path.parent / run['tracePath']
            last, tools = None, []
            for line in trace.read_text().splitlines():
                e = json.loads(line)
                if e.get('type') == 'result':
                    last = e.get('result')
                if e.get('type') == 'assistant':
                    tools += [b for b in e['message']['content'] if b.get('type') == 'tool_use']
            verdicts = {}
            for g in graders:
                if g['type'] == 'regex':
                    r = js([{'id': 'x', 'pattern': g['pattern'], 'flags': g.get('flags', ''), 'match': g.get('match', 'contains'), 'text': last or ''}])['x']
                    verdicts[g['name']] = r['matched'] if last is not None else None
                else:
                    inputs = [json.dumps(t['input']) for t in tools if t['name'] == g['tool']]
                    hits = js([{'id': str(k), 'pattern': g['input_match'], 'text': s} for k, s in enumerate(inputs)]) if inputs else {}
                    n = sum(r['matched'] for r in hits.values())
                    verdicts[g['name']] = g.get('min', 1) <= n <= g.get('max', float('inf'))
            result[f"{case['name']}/run{i}"] = verdicts
json.dump(result, sys.stdout, indent=1)
print()
