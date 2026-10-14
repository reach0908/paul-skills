#!/usr/bin/env python3
"""Copy fixed evaluation inputs. Preparation is not evidence of execution."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from skill_paths import skill_directory
BASE = ROOT / '.scratch/design-role-parity-20261012'
UPSTREAM = Path('/tmp/paul-design-research-20261009/jakubkrehel-skills')
ORIGINALS = {'information-architecture', 'user-flow', 'wireframe', 'design-browser'}


def digest_files(folder):
    return {str(p.relative_to(folder)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(folder.rglob('*')) if p.is_file() and '.git' not in p.parts}


def cases_for(role):
    result = []
    for catalog in sorted((HERE / 'fixtures').glob('*/cases.json')):
        data = json.loads(catalog.read_text())
        if isinstance(data, dict):
            data = data['cases']
        for case in data:
            if case['role'] == role:
                result.append((catalog, case))
    return result


def prepare(role, arm, repeat, suffix=''):
    run_id = f'{role}-{arm}-r{repeat}{suffix}'
    dest = BASE / 'runs' / run_id
    if dest.exists():
        raise ValueError(f'Refusing to overwrite {dest}')
    cases = cases_for(role)
    if len(cases) != 3:
        raise ValueError(f'Expected 3 cases for {role}, got {len(cases)}')
    manifest = json.loads((ROOT / 'evals/design-beta/upstream-manifest.json').read_text())
    selected = sorted({Path(p).parts[1] for p in manifest['files'] if p.endswith('/SKILL.md')})
    bundle = {}
    if arm == 'original':
        for name, expected in manifest['files'].items():
            raw = subprocess.check_output(['git', '-C', str(UPSTREAM), 'show', f'{manifest["revision"]}:{name}'])
            if hashlib.sha256(raw).hexdigest() != expected:
                raise ValueError(f'Upstream mismatch: {name}')
            bundle[name] = raw
        license_data = bundle.pop('LICENSE')
        for name in selected:
            bundle[f'skills/{name}/LICENSE'] = license_data
    elif arm == 'paul':
        for name in [*selected, *sorted(ORIGINALS)]:
            folder = skill_directory(ROOT, name)
            for p in sorted(folder.rglob('*')):
                if p.is_symlink():
                    raise ValueError(f'Unexpected symlink: {p}')
                if p.is_file():
                    bundle[f'skills/{name}/{p.relative_to(folder)}'] = p.read_bytes()
    elif arm != 'control':
        raise ValueError(arm)
    dest.mkdir(parents=True)
    (dest / 'output').mkdir()
    for name, raw in bundle.items():
        p = dest / '.agents' / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(raw)
    mapped = []
    for catalog, case in cases:
        directory = case.get('fixture_directory', case.get('fixture_dir', case.get('fixture_path')))
        src = ROOT / directory
        if not src.exists():
            src = catalog.parent / directory
        if not src.is_dir():
            raise ValueError(f'Missing fixture: {src}')
        target = dest / 'cases' / case['id']
        if catalog.parent.name == 'explicit':
            target.mkdir(parents=True)
            shutil.copy2(src / 'TASK.md', target / 'TASK.md')
            setup = subprocess.check_output([
                'python3', str(catalog.parent / 'prepare.py'), '--case', case['id'],
                '--destination', str(target / 'app')], text=True)
            (target / 'setup-receipt.json').write_text(setup)
        else:
            shutil.copytree(src, target, ignore=shutil.ignore_patterns('case.json', '__pycache__'))
        (target / 'output').mkdir(exist_ok=True)
        url_suffix = 'app/' if (target / 'app').is_dir() else ''
        visible_case = {k: v for k, v in case.items() if k not in ('setup', 'evaluator_criteria_id')}
        mapped.append({**visible_case, 'task': 'TASK.md', 'directory': str(target),
                       'productDirectory': str(target / 'app' if url_suffix else target),
                       'url': f'http://127.0.0.1:48812/runs/{run_id}/cases/{case["id"]}/{url_suffix}'})
    invocation = (f'Use ${role} by reading .agents/skills/{role}/SKILL.md and its applicable references. '
                  'Read a required dependency from this local bundle when needed. '
                  if arm != 'control' else
                  'Complete the tasks with your ordinary capabilities. No design skill is supplied in this condition. ')
    prompt = f'''You are executing a user-authorized design evaluation, not judging the evaluated skill.
Work only in {dest}. {invocation}
Read and solve all three independent requests in the case directories listed in trial.json, in listed order. Read each TASK.md before working. Each directory has its own output. productDirectory names the app or repository root to use for source and Git commands. Git fixtures are already prepared; do not recreate them. Actual user tasks take precedence over generic skill suggestions. A request to use an explicit-only role is authorized in this trial.
Use the supplied task inputs and only the local skill bundle. Do not inspect other trials, evaluator rubrics, source repository skills, previous conclusions or hidden reference implementations. Do not spawn agents. Keep all case outputs separate. Cases share this conversation; repeats and other conditions use fresh conversations.
For browser work the user specifies playwright-cli, which is installed. Read installed help. The local server is already serving the case URLs in trial.json; new local files are immediately available. Use task-owned -s= sessions, at most one session at a time, and preserve CLI commands, errors and real returned observations. Use snapshot before selecting page controls. Structured return from run-code is useful when collecting observations. Request scoped execution permission through the normal tool mechanism if the sandbox prevents localhost or browser startup. Do not bypass sandbox policies. Browser research to external sites and live account writes are outside these local tasks. Close only your own session after each case, unless its task needs an interactive handoff.
Produce the requested actual outputs, not a plan or self-scored pass. Write output/report.md per case in Korean, with concrete observations and limitations. Also write output/execution.json per case: {{"case":"id","status":"completed|partial|blocked","commands":[],"observations":[],"artifacts":[],"failures":[],"unverified":[],"elapsedSeconds":null,"tokens":null,"cost":null}}. Record actual available telemetry; unknown remains null. For review findings also write output/findings.json as an array of objects with domain, issue, location, evidence, severity. It may be empty with explanation in the report. Do not use evaluator criterion IDs or invent measurements.
Timebox roughly 4 minutes per case, 12 minutes total. Finish all3 with honestly bounded results rather than spending the entire run on the first. Keep installed skill files unchanged. Final message lists all3 output reports and unresolved limits.
'''
    (dest / 'PROMPT.md').write_text(prompt)
    record = {'id': run_id, 'role': role, 'arm': arm, 'repeat': repeat,
              'sourceRevision': manifest['revision'] if arm == 'original' else None,
              'cases': mapped, 'status': 'prepared',
              'model': 'inherited, no override', 'effort': 'inherited, no override',
              'context': 'fresh role context; three separate case directories share that context',
              'inputs': digest_files(dest)}
    (dest / 'trial.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    return {'id': run_id, 'directory': str(dest), 'prompt': str(dest / 'PROMPT.md')}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('role')
    parser.add_argument('arm', choices=['original', 'paul', 'control'])
    parser.add_argument('repeat', type=int)
    parser.add_argument('--suffix', default='')
    args = parser.parse_args()
    print(json.dumps(prepare(args.role, args.arm, args.repeat, args.suffix)))
