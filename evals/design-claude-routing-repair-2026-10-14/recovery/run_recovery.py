#!/usr/bin/env python3
"""Run the frozen final-source follow-up after the original matrix finishes."""
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import run_trials as runner
import collect

ORIGINAL_RAW = runner.RAW
for case in json.loads((HERE.parent / 'cases.json').read_text())['cases']:
    p = ORIGINAL_RAW / (case['id'] + '.meta.json')
    if not p.exists() or 'exit_code' not in json.loads(p.read_text()):
        raise RuntimeError('Finish the original matrix before follow-up')
runner.HERE = HERE
runner.RAW = ORIGINAL_RAW / 'recovery'
runner.TRIAL = runner.TRIAL / 'recovery'
runner.BUNDLE = runner.BUNDLE.parent / 'bundle-final'


def total_cost():
    amount = 0
    for p in ORIGINAL_RAW.rglob('*.jsonl'):
        if '.transcript.' in p.name:
            continue
        result = next((e for e in reversed(runner.read_events(p)) if e.get('type') == 'result'), {})
        amount += result.get('total_cost_usd') or 0
    return amount


runner.cost_so_far = total_cost
runner.main()
collect.HERE = HERE
collect.RAW = runner.RAW
collect.OUT = HERE / 'evidence'
collect.CASES = json.loads((HERE / 'cases.json').read_text())['cases']
collect.main()
