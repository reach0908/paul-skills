import json
import os
import select
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path('/private/tmp/paul-first-impression-044-release-20261015')
(ROOT / 'workspace').mkdir(parents=True, exist_ok=True)
OUT = Path(__file__).resolve().parents[2] / '.scratch/first-impression-044-release'
env = dict(os.environ)
workspace = ROOT / 'workspace'
mode = 'catalog'
command = ['codex', 'app-server', '--stdio']
prefix = os.environ.get('PROBE_PREFIX', 'installed-catalog')
proc = subprocess.Popen(command, cwd=workspace, env=env,
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                        stderr=(OUT / 'catalog-stderr.log').open('w'), text=True)
messages = []

def call(number, method, params):
    proc.stdin.write(json.dumps({'id': number, 'method': method, 'params': params}) + '\n')
    proc.stdin.flush()
    deadline = time.monotonic() + 45
    while time.monotonic() < deadline:
        ready, _, _ = select.select([proc.stdout], [], [], 1)
        if not ready:
            continue
        line = proc.stdout.readline()
        if not line:
            raise RuntimeError('App server closed before response')
        message = json.loads(line)
        messages.append(message)
        if message.get('id') == number:
            return message
    raise TimeoutError(method)

try:
    init = call(1, 'initialize', {'clientInfo': {'name': 'paul-design-install-test', 'version': '1.0'}})
    proc.stdin.write(json.dumps({'method': 'initialized'}) + '\n')
    proc.stdin.flush()
    if len(sys.argv) > 1 and sys.argv[1] == 'models':
        result = call(2, 'model/list', {'limit': 100, 'includeHidden': False})
        (OUT / 'models.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps([{'model': m['model'], 'isDefault': m['isDefault'], 'defaultReasoningEffort': m['defaultReasoningEffort']} for m in result.get('result', {}).get('data', [])]))
        sys.exit(0)
    result = call(2, 'skills/list', {'cwds': [str(workspace)], 'forceReload': True})
    (OUT / (prefix + '.json')).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    rows = result.get('result', {}).get('data', [])
    selected = [s for row in rows for s in row.get('skills', []) if '/paul-skills/paul-skills/0.4.4/' in s.get('path', '') and s.get('enabled')]
    (OUT / (prefix + '-selected.json')).write_text(json.dumps(selected, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'selected': len(selected), 'names': [s['name'] for s in selected]}, ensure_ascii=False))
finally:
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
    (OUT / ('models-rpc.json' if mode == 'models' else prefix + '-rpc.json')).write_text(json.dumps(messages, ensure_ascii=False, indent=2) + '\n')
