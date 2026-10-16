"""Minimal CLI/model compatibility probe; one preserved attempt per label."""
from pathlib import Path
import argparse, hashlib, json, os, signal, subprocess, time

HERE = Path(__file__).resolve().parent
RAW = HERE.parents[1] / '.scratch/cli-css-repair-20261015'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--binary', required=True)
    args = parser.parse_args()
    out = RAW / ('compat-' + args.label)
    out.mkdir(exist_ok=False)
    cwd = Path('/private/tmp/paul-cli-compat-20261015') / args.label
    cwd.mkdir(parents=True, exist_ok=False)
    cmd = [args.binary, 'exec', '-c', 'model_reasoning_effort="low"', '--sandbox',
           'read-only', '--skip-git-repo-check', '--json', '-C', str(cwd), '-']
    start = time.monotonic()
    timed_out = False
    with (out / 'events.jsonl').open('w') as stdout, (out / 'stderr.txt').open('w') as stderr:
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=stdout, stderr=stderr,
                                text=True, start_new_session=True)
        try:
            proc.communicate('Reply exactly COMPAT_OK. Do not use tools or inspect files.', timeout=60)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(proc.pid, signal.SIGTERM)
            proc.wait(timeout=5)
    rows = [json.loads(x) for x in (out / 'events.jsonl').read_text().splitlines() if x.startswith('{')]
    messages = [r['item'].get('text', '') for r in rows if r.get('type') == 'item.completed'
                and r.get('item', {}).get('type') == 'agent_message']
    passed = proc.returncode == 0 and any(r['type'] == 'turn.completed' for r in rows) and messages[-1:] == ['COMPAT_OK']
    result = {'label': args.label, 'version': subprocess.check_output([args.binary, '--version'], text=True).strip(),
              'exit_code': proc.returncode, 'timed_out': timed_out, 'passed': passed,
              'duration_seconds': round(time.monotonic() - start, 3),
              'failure': next((r.get('error') for r in rows if r.get('type') == 'turn.failed'), None),
              'events_sha256': hashlib.sha256((out / 'events.jsonl').read_bytes()).hexdigest(),
              'global_model_overridden': False, 'command': cmd}
    (out / 'receipt.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['label', 'version', 'exit_code', 'passed', 'failure']}))
    raise SystemExit(0 if passed else 1)
