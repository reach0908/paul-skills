#!/usr/bin/env python3
"""Rebuild a run's final files: run the case scaffold in a fresh directory, then replay the
trace's Write and Edit calls in order. The runner seals the real workspace, so this is how
final file contents are reviewed. Prints the named file.

usage: replay.py <case> <trace.jsonl> <relative file> <empty out dir>
"""
import json
import subprocess
import sys
from pathlib import Path

case, trace, rel, out = sys.argv[1], Path(sys.argv[2]), sys.argv[3], Path(sys.argv[4])
out.mkdir(parents=True)
subprocess.run(['bash', str(Path(__file__).parent / 'cases' / case / 'scaffold.sh')], cwd=out, check=True)
cwd = None
for line in trace.read_text().splitlines():
    event = json.loads(line)
    if event.get('type') == 'system' and event.get('subtype') == 'init':
        cwd = event['cwd']
    if event.get('type') != 'assistant':
        continue
    for block in event['message'].get('content', []):
        if block.get('type') != 'tool_use' or block['name'] not in ('Write', 'Edit'):
            continue
        inp = block['input']
        target = out / Path(inp['file_path']).relative_to(cwd)
        if block['name'] == 'Write':
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(inp['content'])
        else:
            text = target.read_text()
            if inp['old_string'] not in text:
                print(f'# edit did not apply: {inp["old_string"][:60]!r}', file=sys.stderr)
                continue
            count = -1 if inp.get('replace_all') else 1
            target.write_text(text.replace(inp['old_string'], inp['new_string'], count))
print((out / rel).read_text())
