"""Run the stored CLI scenario and propagate structured failures to the shell."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--session', required=True)
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--mutation', choices=['missing-option', 'no-tab', 'blocked-keys', 'overflow'])
args = parser.parse_args()
source = Path(__file__).with_name('check_browser.js').read_text()
if args.mutation:
    source = source.replace('const mutation = null;', f'const mutation = {json.dumps(args.mutation)};')
with tempfile.TemporaryDirectory(prefix='paul-keyboard-check-') as temp:
    script = Path(temp) / 'check.js'
    script.write_text(source)
    process = subprocess.run(['playwright-cli', f'-s={args.session}', 'run-code', f'--filename={script}', '--raw'], text=True, capture_output=True)
try:
    result = json.loads(process.stdout)
except json.JSONDecodeError:
    result = {'status': 'runner-error', 'stdout': process.stdout, 'stderr': process.stderr}
result['cliExitCode'] = process.returncode
args.output.write_text(json.dumps(result, indent=2) + '\n')
passed = process.returncode == 0 and result.get('status') == 'passed' and len(result.get('results', [])) == 8
print(json.dumps({'status':result.get('status'), 'cases':len(result.get('results', [])), 'failures':[r for r in result.get('results', []) if r.get('status') != 'passed'], 'output':str(args.output)}))
sys.exit(0 if passed else 1)
