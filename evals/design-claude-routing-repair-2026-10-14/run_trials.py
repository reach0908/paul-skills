#!/usr/bin/env python3
"""Run frozen cases in fresh Claude processes with an identified plugin source."""
import argparse
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import time
import uuid

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
RAW = REPO / '.scratch/design-claude-routing-repair-20261014'
TRIAL = Path('/private/tmp/paul-design-claude-routing-repair-20261014')
BUNDLE = TRIAL / 'bundle'
CACHE = Path.home() / '.claude/plugins/cache/paul-skills/paul-skills/0.4.0'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_events(path):
    events = []
    for line in path.read_text().splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events


def snapshot(path):
    return {str(p.relative_to(path)): digest(p.read_bytes())
            for p in sorted(path.rglob('*')) if p.is_file()}


def prepare_fixture(cwd):
    def git(*args):
        return subprocess.check_output(['git', '-c', 'core.hooksPath=/dev/null', *args], cwd=cwd, stderr=subprocess.STDOUT)
    git('init', '-q', '-b', 'main')
    (cwd / 'src').mkdir()
    (cwd / 'src/Panel.html').write_text((HERE / 'fixtures/before.html').read_text())
    git('add', 'src/Panel.html')
    git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', '-c', 'commit.gpgsign=false', 'commit', '-qm', 'Initial screen')
    git('switch', '-qc', 'feature/checkout')
    (cwd / 'src/Panel.html').write_text((HERE / 'fixtures/after.html').read_text())


def run(case):
    case_id = case['id']
    meta_path = RAW / f'{case_id}.meta.json'
    if meta_path.exists():
        raise RuntimeError(f'Refusing to replace existing run: {case_id}')
    case_order = [c['id'] for c in json.loads((HERE / 'cases.json').read_text())['cases']]
    cwd = TRIAL / f'case_{case_order.index(case_id) + 1:03d}'
    cwd.mkdir(parents=True, exist_ok=False)
    if case.get('fixture') == 'git':
        prepare_fixture(cwd)
    sid = str(uuid.uuid4())
    command = ['claude', '-p', '--verbose', '--output-format', 'stream-json',
               '--input-format', 'stream-json', '--replay-user-messages',
               '--session-id', sid, '--permission-mode', 'dontAsk',
               '--tools', 'Skill,Read,Glob,Grep',
               '--allowedTools', 'Skill,Read,Glob,Grep', '--strict-mcp-config',
               '--settings', '{"disableAllHooks":true}', '--max-budget-usd', str(case.get('max_cost', 0.80))]
    if case.get('arm') != 'baseline':
        command.extend(['--plugin-dir', str(BUNDLE)])
    if case['mode'] == 'handoff':
        command[command.index('--tools') + 1] += ',Bash'
        command[command.index('--allowedTools') + 1] += ',' + ','.join('Bash(git ' + verb + ' *)' for verb in ['status', 'diff', 'show', 'rev-parse', 'log', 'ls-files', 'blame', 'remote', 'branch', 'merge-base', 'symbolic-ref'])
    if case.get('extra_read_shell'):
        command[command.index('--allowedTools') + 1] += ',' + ','.join(case['extra_read_shell'])
    meta = {'arm': case.get('arm', 'candidate'), 'plugin_root': str(CACHE if case.get('arm') == 'baseline' else BUNDLE), 'bundle_manifest_sha256': digest((HERE / 'bundle-manifest.json').read_bytes()), 'case_id': case_id, 'session_id': sid, 'command': command,
            'cwd': str(cwd), 'prompt': case['prompt'],
            'case_sha256': digest(json.dumps(case, ensure_ascii=False, sort_keys=True).encode()),
            'started_at': datetime.now(timezone.utc).isoformat(),
            'files_before': snapshot(cwd),
            'protocol_sha256': digest((HERE / 'PROTOCOL.md').read_bytes()),
            'cases_sha256': digest((HERE / 'cases.json').read_bytes())}
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + '\n')
    start = time.monotonic()
    timed_out = False
    with (RAW / f'{case_id}.jsonl').open('w') as out, (RAW / f'{case_id}.stderr').open('w') as err:
        proc = subprocess.Popen(command, cwd=cwd, stdin=subprocess.PIPE,
                                stdout=out, stderr=err, text=True, start_new_session=True)
        payload = json.dumps({'type': 'user', 'message': {'role': 'user', 'content': case['prompt']}}) + '\n'
        try:
            proc.communicate(payload, timeout=case.get('timeout_seconds', 360))
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(proc.pid, signal.SIGTERM)
            try:
                proc.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.communicate()
    meta.update(exit_code=proc.returncode, timed_out=timed_out,
                duration_seconds=round(time.monotonic() - start, 3),
                files_after=snapshot(cwd), finished_at=datetime.now(timezone.utc).isoformat())
    transcripts = list((Path.home() / '.claude/projects').glob(f'*/{sid}.jsonl'))
    if len(transcripts) == 1:
        shutil.copyfile(transcripts[0], RAW / f'{case_id}.transcript.jsonl')
        meta['transcript_sha256'] = digest(transcripts[0].read_bytes())
    else:
        meta['transcript_error'] = f'Expected one transcript, found {len(transcripts)}'
    events = read_events(RAW / f'{case_id}.jsonl')
    result = next((e for e in reversed(events) if e.get('type') == 'result'), {})
    meta.update(total_cost_usd=result.get('total_cost_usd'), result_subtype=result.get('subtype'))
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: meta[k] for k in ['case_id', 'exit_code', 'timed_out', 'duration_seconds', 'total_cost_usd', 'result_subtype']}), flush=True)
    return meta


def cost_so_far():
    cost = 0
    for p in RAW.glob('*.jsonl'):
        if '.transcript.' in p.name:
            continue
        result = next((e for e in reversed(read_events(p)) if e.get('type') == 'result'), {})
        cost += result.get('total_cost_usd') or 0
    return cost


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['explicit', 'implicit', 'boundary', 'handoff'])
    parser.add_argument('--id')
    args = parser.parse_args()
    RAW.mkdir(parents=True, exist_ok=True)
    cases = json.loads((HERE / 'cases.json').read_text())['cases']
    selected = [c for c in cases if (args.mode is None or c['mode'] == args.mode)
                and (not args.id or c['id'] == args.id)
                and not (RAW / f"{c['id']}.meta.json").exists()]
    failures = 0
    with ThreadPoolExecutor(max_workers=2) as pool:
        pending = set()
        offset = 0
        while pending or offset < len(selected):
            while len(pending) < 2 and offset < len(selected):
                if cost_so_far() >= 22:
                    raise RuntimeError('Experiment cost stop reached')
                pending.add(pool.submit(run, selected[offset]))
                offset += 1
            completed, pending = wait(pending, return_when=FIRST_COMPLETED)
            for future in completed:
                result = future.result()
                failures = failures + 1 if result['exit_code'] or result['timed_out'] else 0
                if failures >= 2:
                    raise RuntimeError('Repeated environment failure; inspect before resuming')
    print(json.dumps({'estimated_list_cost_usd': cost_so_far()}))


if __name__ == '__main__':
    main()
