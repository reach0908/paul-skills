#!/usr/bin/env python3
"""Tooling for the `claude plugin eval` suite in evals/claude-native.

check              static suite consistency plus regex and input_match controls (no model calls)
plan               zero-cost `claude plugin eval` plan check for every group (needs the claude CLI)
record AGG         turn an aggregate-result.json into a rubric verdict record
calibration-cases  write grader calibration cases from the labelled artifacts
calibrate AGG      compare a calibration run with the expected verdicts

The native score is a weighted fraction of passed graders. This tooling never uses it as a verdict:
a required failure is not offset, unjudged graders stay unknown and errored runs are excluded, not zero.
Standard library only; JavaScript regex semantics are delegated to node.
"""
import argparse
import fnmatch
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUITE_DIR = HERE.parent
ROOT = SUITE_DIR.parents[1]
PAID = {'llm', 'baseline'}
DETERMINISTIC_TEXT = {'regex'}
GATED = {'Bash', 'Write', 'Edit', 'WebFetch', 'WebSearch', 'NotebookEdit'}
ARTIFACT_DELIMITER = 'PAUL_EVAL_ARTIFACT'
CALIBRATION_PROMPT = 'This is a grader calibration run. Do not use any tool. Reply with the single word: done.'
LAST_MESSAGE_FILE = 'calibration/last-message.md'


def load(suite_dir=SUITE_DIR):
    suite = json.loads((suite_dir / 'suite.json').read_text())
    rubric = json.loads((suite_dir / suite['rubric']).read_text())
    cases = {}
    for path in sorted(suite_dir.glob('*/case.yaml')):
        # case.yaml is written in JSON-compatible YAML so CI can read it without a YAML library.
        cases[path.parent.name] = json.loads(path.read_text())
    return suite, rubric, cases


def criterion_of(name, rubric):
    prefix = name.split('-', 1)[0]
    if prefix == 'IND':
        return 'IND'
    return prefix if prefix in rubric['criteria'] else None


def target_of(grader):
    value = grader.get('target') if grader['type'] == 'regex' else grader.get('focus')
    if value is None:
        return 'last_message' if grader['type'] in ('regex', 'llm') else None
    if isinstance(value, dict) and value.get('source') == 'file':
        return value['path']
    return value


def group_of(case, suite):
    groups = [tag for tag in case.get('tags', []) if tag in suite['groups']]
    return groups[0] if len(groups) == 1 else None


def check_static(suite_dir=SUITE_DIR):
    suite, rubric, cases = load(suite_dir)
    problems = []
    profiles = suite['cases']
    for name in sorted(set(cases) ^ set(profiles)):
        problems.append(f'{name}: case directory and suite.json profile must both exist')
    for name in sorted(set(cases) & set(profiles)):
        case, profile = cases[name], profiles[name]
        where = f'{name}:'
        if case.get('schema_version') != '1.1' or case.get('name') != name:
            problems.append(f'{where} schema_version must be "1.1" and name must match the directory')
        group = group_of(case, suite)
        if group is None:
            problems.append(f'{where} needs exactly one group tag from suite.json')
        case_dir = suite_dir / name
        if not (case_dir / 'prompt.md').exists() and not case.get('execution', {}).get('prompt'):
            problems.append(f'{where} has no prompt')
        script = case.get('context', {}).get('scaffold_script')
        if script and not (case_dir / script).is_file():
            problems.append(f'{where} scaffold_script {script} is missing')
        in_scope = {cid for cid, c in rubric['criteria'].items() if c['scope'] in ('common', profile['skill'])}
        classified = set(profile['required']) | set(profile['notApplicable']) | set(profile['quality'])
        for cid in sorted(classified - set(rubric['criteria'])):
            problems.append(f'{where} {cid} is not in the rubric')
        for cid in sorted(in_scope - classified):
            problems.append(f'{where} {cid} must be required, quality or notApplicable with a reason')
        for cid in sorted(set(profile['required']) & set(profile['notApplicable'])):
            problems.append(f'{where} {cid} is both required and not applicable')
        for cid, reason in profile['notApplicable'].items():
            if not reason.strip():
                problems.append(f'{where} {cid} needs a not-applicable reason')
        for cid in profile['quality']:
            if rubric['criteria'].get(cid, {}).get('kind') != 'quality':
                problems.append(f'{where} {cid} is listed as quality but the rubric says otherwise')
        for cid in sorted(set(profile['human']) - set(profile['required'])):
            problems.append(f'{where} human criterion {cid} is not required')
        for cid in sorted(set(profile['harnessEnforced']) - set(profile['required'])):
            problems.append(f'{where} harness-enforced criterion {cid} is not required')
        for cid in sorted(set(profile.get('notApplicableWithout', {})) - set(profile['required'])):
            problems.append(f'{where} notApplicableWithout criterion {cid} is not required')
        names = [g['name'] for g in case.get('graders', [])]
        if len(names) != len(set(names)):
            problems.append(f'{where} grader names must be unique')
        mapped = {}
        allowed = set(case.get('execution', {}).get('allowed_tools', []))
        for grader in case.get('graders', []):
            cid = criterion_of(grader['name'], rubric)
            if cid is None:
                problems.append(f'{where} grader {grader["name"]} must start with a rubric ID or IND-')
                continue
            if cid != 'IND':
                mapped.setdefault(cid, []).append(grader)
                if cid not in profile['required']:
                    problems.append(f'{where} grader {grader["name"]} grades {cid}, which is not required here')
            if grader['type'] == 'tool_used' and 'max' in grader and grader.get('min', 1) > grader['max']:
                problems.append(f'{where} grader {grader["name"]} can never pass: tool_used min defaults to 1, so max {grader["max"]} needs an explicit min')
            for tool in [grader.get('tool')] + [side.get('tool') for side in (grader.get('before'), grader.get('after')) if isinstance(side, dict)]:
                if tool and tool not in allowed:
                    problems.append(f'{where} grader {grader["name"]} observes {tool}, which allowed_tools withholds, so it measures nothing')
        for tool in sorted(allowed & GATED):
            grants = suite['groups'].get(group, {}).get('allowTools', []) if group else []
            if not any(g == tool or g.startswith(tool + '(') for g in grants):
                problems.append(f'{where} {tool} is in allowed_tools but the group grant does not include it')
        file_tools = {'Edit', 'Write'}
        zero_calls = {(g.get('tool'), g.get('input_match')) for g in case.get('graders', [])
                      if g['type'] == 'tool_used' and g.get('max') == 0}
        for grader in case.get('graders', []):
            sides = [grader] if grader['type'] == 'tool_used' else [s for s in (grader.get('before'), grader.get('after')) if isinstance(s, dict)]
            touched = [s for s in sides if s.get('tool') in file_tools]
            for side in touched:
                if not str(side.get('input_match', '')).startswith('"file_path"'):
                    problems.append(f'{where} grader {grader["name"]} must anchor its Edit/Write input_match to "file_path"; the JSON input also holds file contents')
            if touched and not (grader['type'] == 'tool_used' and grader.get('max') == 0):
                problems.append(f'{where} grader {grader["name"]} needs a file change from one tool, but Edit permission also allows Write; use traceChecks')
            if grader['type'] == 'tool_used' and grader.get('tool') in file_tools and grader.get('max') == 0:
                twin = ({'Edit', 'Write'} - {grader['tool']}).pop()
                if (twin, grader.get('input_match')) not in zero_calls:
                    problems.append(f'{where} grader {grader["name"]} forbids {grader["tool"]} but has no matching {twin} grader')
        for check in profile.get('traceChecks', []):
            cid = criterion_of(check['name'], rubric)
            if cid in (None, 'IND') or cid not in profile['required']:
                problems.append(f'{where} trace check {check["name"]} must name a required criterion')
            else:
                mapped.setdefault(cid, []).append({'name': check['name'], 'type': 'trace'})
            specs = [check.get('match')] if check['type'] == 'count' else [check.get('before'), check.get('after')]
            if check['type'] not in ('count', 'order') or not all(isinstance(s, dict) for s in specs):
                problems.append(f'{where} trace check {check["name"]} must be a count with match or an order with before and after')
                continue
            for spec in specs:
                if set(spec) - {'tools', *TRACE_FIELDS} or not spec.get('tools'):
                    problems.append(f'{where} trace check {check["name"]} uses unknown fields {sorted(set(spec) - {"tools", *TRACE_FIELDS})}')
                for tool in spec.get('tools', []):
                    if tool not in allowed:
                        problems.append(f'{where} trace check {check["name"]} observes {tool}, which allowed_tools withholds')
        for cid in profile['required']:
            if cid not in mapped and cid not in profile['human'] and cid not in profile['harnessEnforced']:
                problems.append(f'{where} required {cid} has no grader, human judgement or harness enforcement')
        for grader in case.get('graders', []):
            if grader['type'] not in PAID:
                continue
            cid, target = criterion_of(grader['name'], rubric), target_of(grader)
            seen = {item['expect'].get(cid) for item in profile.get('calibration', []) if item['target'] == target}
            if not {True, False} <= seen:
                problems.append(f'{where} llm grader {grader["name"]} needs a pass and a fail calibration artifact for {cid} on {target}')
        for item in profile.get('calibration', []):
            label = f'{where} calibration {item["label"]}'
            if not (suite_dir / item['artifact']).is_file():
                problems.append(f'{label} artifact is missing')
            for cid, expected in item['expect'].items():
                if cid not in profile['required']:
                    problems.append(f'{label} expects {cid}, which is not required')
                if expected != 'human' and not any(target_of(g) == item['target'] for g in mapped.get(cid, [])):
                    problems.append(f'{label} expects {cid} but no {cid} grader reads {item["target"]}')
    for control in suite.get('inputControls', []):
        graders = {g['name']: g for g in cases.get(control['case'], {}).get('graders', [])}
        grader = graders.get(control['grader'])
        if grader is None or grader['type'] not in ('tool_used', 'tool_order'):
            problems.append(f'input control names unknown tool grader {control["case"]}:{control["grader"]}')
    staged = suite_dir / 'interface-review-staged/scaffold.sh'
    for other in sorted(suite_dir.glob('interface-review-*/scaffold.sh')):
        if staged.exists() and other != staged and other.read_bytes() != staged.read_bytes():
            problems.append(f'{other.parent.name}/scaffold.sh must stay identical to interface-review-staged/scaffold.sh')
    for path in sorted(suite_dir.rglob('*')):
        parts = path.relative_to(suite_dir).parts
        machine_record = parts[0] == 'records' and path.suffix == '.json'
        if path.is_file() and 'results' not in parts and '__pycache__' not in parts and not machine_record:
            if chr(0x2014) in path.read_text(errors='replace'):
                problems.append(f'em dash in {path.relative_to(suite_dir)}')
    return problems


def run_node(items):
    node = shutil.which('node')
    if node is None:
        raise RuntimeError('node is required for regex controls')
    out = subprocess.run([node, str(HERE / 'regex_eval.mjs')], input=json.dumps(items), capture_output=True, text=True, check=True)
    return {r['id']: r for r in json.loads(out.stdout)}


def deterministic_controls(suite_dir=SUITE_DIR):
    """Check regex graders against the labelled artifacts and input_match patterns against sample inputs."""
    suite, rubric, cases = load(suite_dir)
    items, meta = [], {}
    for name, profile in suite['cases'].items():
        for item in profile.get('calibration', []):
            text = (suite_dir / item['artifact']).read_text()
            for grader in cases[name]['graders']:
                if grader['type'] in DETERMINISTIC_TEXT and target_of(grader) == item['target']:
                    key = f'{name}/{item["label"]}/{grader["name"]}'
                    items.append({'id': key, 'pattern': grader['pattern'], 'flags': grader.get('flags', ''),
                                  'match': grader.get('match', 'contains'), 'text': text})
                    meta[key] = (name, item, grader)
    for i, control in enumerate(suite.get('inputControls', [])):
        grader = next(g for g in cases[control['case']]['graders'] if g['name'] == control['grader'])
        pattern = grader.get('input_match')
        if grader['type'] == 'tool_order':
            pattern = grader[control.get('side', 'before')].get('input_match')
        key = f'input/{i}'
        items.append({'id': key, 'pattern': pattern, 'text': json.dumps(control['input'], ensure_ascii=False, separators=(',', ':'))})
        meta[key] = control
    results = run_node(items)
    problems = []
    for key, result in results.items():
        if result.get('error'):
            problems.append(f'{key}: {result["error"]}')
    for i, control in enumerate(suite.get('inputControls', [])):
        if results[f'input/{i}']['matched'] != control['matches']:
            problems.append(f'input control {control["case"]}:{control["grader"]} on {control["input"]} should '
                            f'{"" if control["matches"] else "not "}match')
    for name, profile in suite['cases'].items():
        for item in profile.get('calibration', []):
            for cid, expected in item['expect'].items():
                graders = [g for g in cases[name]['graders'] if criterion_of(g['name'], rubric) == cid and target_of(g) == item['target']]
                det = [results[f'{name}/{item["label"]}/{g["name"]}']['matched'] for g in graders if g['type'] in DETERMINISTIC_TEXT]
                if expected is True and not all(det):
                    problems.append(f'{name} {item["label"]}: a {cid} regex grader fails a known-good artifact')
                if expected is False and det and len(det) == len(graders) and all(det):
                    problems.append(f'{name} {item["label"]}: {cid} has only regex graders and all pass a known-bad artifact')
    return problems


STAGE_MARKER = '.paul-eval-stage.json'


def stage(out_dir, eval_dirs, root=ROOT):
    """Copy only the plugin manifest, its skills and the eval directories into out_dir.

    The runner refuses plugin directories with more than 20000 entries, and a small copy also keeps
    other trial records out of the candidate's reach. The marker records exactly what was staged.
    """
    import hashlib
    from datetime import datetime, timezone
    out_dir = Path(out_dir)
    if out_dir.exists():
        if not (out_dir / STAGE_MARKER).exists():
            raise ValueError(f'{out_dir} exists and is not a stage directory; refusing to replace it')
        shutil.rmtree(out_dir)
    manifest = json.loads((root / '.claude-plugin/plugin.json').read_text())
    paths = ['.claude-plugin'] + [p[2:] if p.startswith('./') else p for p in manifest['skills']] + list(eval_dirs)
    ignore = shutil.ignore_patterns('results', '__pycache__', '.DS_Store')
    for rel in paths:
        src = root / rel
        if not src.exists():
            raise ValueError(f'{rel} does not exist')
        shutil.copytree(src, out_dir / rel, ignore=ignore)
    files = {}
    for p in sorted(out_dir.rglob('*')):
        if p.is_file():
            files[p.relative_to(out_dir).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    digest = hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()
    rubric = json.loads((root / 'evals/claude-native/rubric.json').read_text())
    marker = {'createdAt': datetime.now(timezone.utc).isoformat(), 'source': str(root),
              'repository': repository_state(rubric, root), 'paths': paths,
              'fileCount': len(files), 'digest': f'sha256:{digest}'}
    (out_dir / STAGE_MARKER).write_text(json.dumps(marker, indent=2) + '\n')
    return marker


def group_command(suite, group, extra):
    if group == 'calibration':
        return ['claude', 'plugin', 'eval', '.', '--eval-dir', suite['calibrationDir'], '--ablation', 'none',
                '--scaffold', '--no-publish', '--trust-plugin', *extra]
    spec = suite['groups'][group]
    cmd = ['claude', 'plugin', 'eval', '.', '--eval-dir', suite['evalDir'], '--tag', group,
           '--ablation', spec['ablation'], '--scaffold', '--no-publish', '--trust-plugin', *extra]
    if spec['allowTools']:
        cmd += ['--allow-tools', *spec['allowTools']]
    return cmd


def run_group(group, out, stage_dir, extra, suite_dir=SUITE_DIR, root=ROOT):
    """Stage the plugin, run one group (or the calibration suite) and write <out> plus <out>.meta.json."""
    from datetime import datetime, timezone
    suite, _, _ = load(suite_dir)
    eval_dirs = [suite['calibrationDir']] if group == 'calibration' else [suite['evalDir']]
    if group == 'calibration':
        calibration_cases(root / suite['calibrationDir'], suite_dir)
    marker = stage(stage_dir, eval_dirs, root)
    out = Path(out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    keep = [] if '--keep-temp' in extra or group == 'calibration' else ['--keep-temp']
    cmd = group_command(suite, group, [*extra, *keep, '--json', str(out)])
    started = datetime.now(timezone.utc).isoformat()
    with open(str(out) + '.log', 'w') as log:
        code = subprocess.run(cmd, cwd=stage_dir, stdout=log, stderr=subprocess.STDOUT).returncode
    if out.exists() and group != 'calibration':
        # Kept run directories live under /tmp; copy each trace next to the result so records survive cleanup.
        for case in json.loads(out.read_text()).get('cases', []):
            for arm, runs in case['arms'].items():
                for i, r in enumerate(runs or []):
                    src = Path(r.get('tracePath') or '')
                    if src.is_file():
                        dest = Path(str(out) + '.traces') / case['name'] / f'{arm}-{i}.jsonl'
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copyfile(src, dest)
    meta = {'group': group, 'command': cmd, 'cwd': str(stage_dir), 'startedAt': started,
            'finishedAt': datetime.now(timezone.utc).isoformat(), 'exitCode': code,
            'stage': {k: marker[k] for k in ('digest', 'fileCount', 'repository')}}
    if group != 'calibration':
        meta['grants'] = suite['groups'][group]['allowTools']
    Path(str(out) + '.meta.json').write_text(redact(json.dumps(meta, indent=2) + '\n'))
    return code, meta


def plan(suite_dir=SUITE_DIR, root=ROOT):
    """Zero-cost plan check: the cost ceiling 0 stops before the first run, after cases are parsed and planned."""
    import tempfile
    suite, _, _ = load(suite_dir)
    problems = []
    with tempfile.TemporaryDirectory() as tmp:
        stage_dir = Path(tmp) / 'stage'
        stage(stage_dir, [suite['evalDir']], root)
        for group in suite['groups']:
            cmd = group_command(suite, group, ['--max-cost-usd', '0', '--output-dir', str(Path(tmp) / group)])
            out = subprocess.run(cmd, cwd=stage_dir, capture_output=True, text=True)
            text = out.stdout + out.stderr
            bad = [line for line in text.splitlines() if 'cannot pass' in line or 'failed to load' in line or line.startswith('✗')]
            if out.returncode not in (0, 2) or bad:
                problems.append(f'{group}: exit {out.returncode}\n' + '\n'.join(bad or text.splitlines()[-10:]))
    return problems


def combine(values):
    if 'fail' in values:
        return 'fail'
    if 'unknown' in values:
        return 'unknown'
    return 'pass'


def git(*args, root=ROOT):
    out = subprocess.run(['git', '-C', str(root), *args], capture_output=True, text=True)
    return out.stdout.strip() if out.returncode == 0 else None


def repository_state(rubric, root=ROOT):
    paths = [c['path'] for c in rubric['contracts'].values()]
    dirty = git('status', '--porcelain', '--', *paths, 'evals/claude-native', '.claude-plugin', root=root)
    return {
        'head': git('rev-parse', 'HEAD', root=root),
        'skillTrees': {name: git('rev-parse', f'HEAD:{c["path"]}', root=root) for name, c in rubric['contracts'].items()},
        'rubricContractRevision': rubric['contractRevision'],
        'dirtyPaths': dirty.splitlines() if dirty else [],
    }


def load_humans(path):
    if path is None:
        return {}
    data = json.loads(Path(path).read_text())
    return {(r['case'], r['arm'], r['run']): dict(r, reviewer=r.get('reviewer', data.get('reviewer'))) for r in data['reviews']}


def criteria_sha(text):
    import hashlib
    return hashlib.sha256((text or '').encode()).hexdigest() if text else None


def calibrated(status, case, grader, judge_model, criteria=None):
    """Calibration counts only for the same judge model and the exact criteria text that was calibrated."""
    sha = criteria_sha(criteria)
    graders = status.get('graders', {})
    # Earlier criteria versions stay calibrated for records judged with them: "<case>:<grader>@<sha>".
    entry = graders.get(f'{case}:{grader}@{sha}') or graders.get(f'{case}:{grader}')
    return bool(entry and judge_model and status.get('judgeModel') == judge_model
                and entry.get('criteriaSha256') and entry['criteriaSha256'] == sha
                and entry['agreed'] > 0 and entry['falsePass'] == 0 and entry['falseFail'] == 0)


TRACE_FIELDS = {'path': 'file_path', 'command': 'command', 'skill': 'skill'}


def trace_events(path):
    """Tool calls from a run trace in order, as (tool, input) pairs."""
    events = []
    with open(path) as f:
        for line in f:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            message = d.get('message') if isinstance(d, dict) else None
            content = message.get('content') if isinstance(message, dict) else None
            if d.get('type') == 'assistant' and isinstance(content, list):
                events += [(c.get('name'), c.get('input') or {}) for c in content if c.get('type') == 'tool_use']
    return events


def _trace_match(event, spec):
    tool, inp = event
    if tool not in spec['tools']:
        return False
    return all(re.search(spec[f], str(inp.get(key, ''))) for f, key in TRACE_FIELDS.items() if f in spec)


def trace_check(check, events):
    """Evaluate one traceChecks entry. Fields are matched one by one, never the whole JSON input,
    so file contents and import lines cannot satisfy a path pattern."""
    if check['type'] == 'count':
        n = sum(_trace_match(e, check['match']) for e in events)
        low, high = check.get('min', 0), check.get('max')
        return low <= n and (high is None or n <= high), f'{n} matching calls (expected {low}..{"any" if high is None else high})'
    hits = lambda spec: [i for i, e in enumerate(events) if _trace_match(e, spec)]
    before, after = hits(check['before']), hits(check['after'])
    if not before or not after:
        return False, f'{"after" if not after else "before"} call never happened'
    if check.get('mode', 'first') == 'followed':
        return after[-1] > before[0], f'first before call #{before[0]}, last after call #{after[-1]}'
    return before[0] < after[0], f'first before call #{before[0]}, first after call #{after[0]}'


def trace_rows(profile, run, trace_path=None):
    checks = profile.get('traceChecks', [])
    if not checks:
        return []
    path = trace_path or run.get('tracePath')
    try:
        events = trace_events(path)
    except (OSError, TypeError):
        return [{'name': c['name'], 'type': 'trace', 'value': 'unknown', 'explanation': 'trace unavailable'} for c in checks]
    rows = []
    for c in checks:
        ok, why = trace_check(c, events)
        rows.append({'name': c['name'], 'type': 'trace', 'value': 'pass' if ok else 'fail', 'explanation': why})
    return rows


def judge_run(name, profile, ran_graders, run, human, rubric, status, judge_model, arm='with', trace_path=None):
    cost = {'usd': run.get('costUsd'), 'judgeUsd': run.get('judgeCostUsd'), 'turns': run.get('turns'),
            'durationSeconds': run.get('durationSeconds'), 'tokens': None}
    if run.get('error') or run.get('aborted'):
        reason = run.get('error') or f'aborted by mock: {run["aborted"]}'
        return {'status': 'excluded', 'reason': reason, 'verdict': 'excluded', 'cost': cost}
    # Grader types come from the aggregate, which records what actually ran, not the current case file.
    types = {g['name']: g['type'] for g in ran_graders}
    texts = {g['name']: g.get('graderMarkdown') or g.get('criteria') for g in ran_graders}
    evidence, indicators = {}, {}
    for g in run['graders']:
        cid = criterion_of(g['name'], rubric)
        gtype = types.get(g['name'], 'unknown')
        unjudged = gtype in PAID and run.get('skippedPaidGraders')
        value = 'unknown' if unjudged else ('pass' if g['passed'] else 'fail')
        row = {'name': g['name'], 'type': gtype, 'value': value, 'scoredNatively': g.get('scored', True),
               'explanation': g.get('explanation'), 'judgeVotes': g.get('judgeVotes')}
        if gtype in PAID and value != 'unknown':
            row['calibrated'] = calibrated(status, name, g['name'], judge_model, texts.get(g['name']))
        if cid == 'IND':
            indicators[g['name']] = value
        elif cid:
            evidence.setdefault(cid, []).append(row)
    for row in trace_rows(profile, run, trace_path):
        evidence.setdefault(criterion_of(row['name'], rubric), []).append(row)
    human = human or {}
    criteria = {}
    skip = profile.get('notApplicableWithout', {}) if arm == 'without' else {}
    for cid in profile['required']:
        if cid in skip:
            criteria[cid] = {'verdict': 'n/a', 'reason': skip[cid], 'graders': evidence.get(cid, []), 'human': None,
                             'provisional': False, 'basis': 'not applicable without the plugin'}
            continue
        rows = evidence.get(cid, [])
        values = [r['value'] for r in rows]
        hv = human.get('criteria', {}).get(cid)
        if hv:
            values.append(hv)
        if 'fail' in values or 'unknown' in values:
            verdict = combine(values)
        elif cid in profile['human'] and not hv:
            verdict = 'pending_human'
        elif values:
            verdict = 'pass'
        elif cid in profile['harnessEnforced']:
            verdict = 'pass'
        else:
            verdict = 'unknown'
        deciding = [r for r in rows if r['value'] == verdict] if verdict in ('pass', 'fail') else []
        provisional = any(r.get('calibrated') is False for r in deciding) and not hv
        criteria[cid] = {'verdict': verdict, 'graders': rows, 'human': hv, 'provisional': provisional,
                         'basis': 'harness' if not rows and not hv and cid in profile['harnessEnforced'] else None}
    values = [c['verdict'] for c in criteria.values()]
    quality = {q: human.get('quality', {}).get(q, 'pending_human') for q in profile['quality']}
    if 'fail' in values:
        verdict = 'fail'
    elif 'unknown' in values:
        verdict = 'undetermined'
    elif 'pending_human' in values:
        verdict = 'pending_human'
    elif 'pending_human' in quality.values():
        verdict = 'required_pass'
    elif 'rewrite' in quality.values():
        verdict = 'quality_hold'
    else:
        verdict = 'pass'
    return {'status': 'judged', 'verdict': verdict,
            'provisional': any(c['provisional'] for c in criteria.values()),
            'criteria': criteria, 'quality': quality, 'indicators': indicators,
            'taskStatus': human.get('taskStatus', 'pending_human'), 'cost': cost,
            'reviewer': human.get('reviewer')}


def summarize(runs):
    summary = {'runs': len(runs), 'excluded': sum(r['status'] == 'excluded' for r in runs), 'verdicts': {}, 'criteria': {}}
    for r in runs:
        summary['verdicts'][r['verdict']] = summary['verdicts'].get(r['verdict'], 0) + 1
        for cid, c in r.get('criteria', {}).items():
            counts = summary['criteria'].setdefault(cid, {})
            counts[c['verdict']] = counts.get(c['verdict'], 0) + 1
    def total(key):
        values = [r['cost'][key] for r in runs if r['cost'].get(key) is not None]
        return round(sum(values), 6) if values else None
    summary['cost'] = {'usd': total('usd'), 'judgeUsd': total('judgeUsd'), 'turns': total('turns'),
                       'durationSeconds': total('durationSeconds'), 'tokens': None,
                       'tokensReason': 'aggregate-result.json schema 1 reports no token usage'}
    return summary


def record(aggregate, human_path=None, suite_dir=SUITE_DIR, root=ROOT, meta=None, trace_dir=None):
    suite, rubric, cases = load(suite_dir)
    status_path = suite_dir / 'calibration/status.json'
    status = json.loads(status_path.read_text()) if status_path.exists() else {}
    humans = load_humans(human_path)
    run_meta, meta = meta, aggregate['suite']
    judge_model = meta.get('judgeModel')
    out_cases, unresolved = [], set()
    if rubric['goldStatus'] != 'human_confirmed':
        unresolved.add('gold_not_human_confirmed')
    if aggregate.get('partial'):
        unresolved.add(f'partial_run:{aggregate.get("partialReason")}')
    if not judge_model:
        unresolved.add('judge_model_not_pinned')
    if not meta.get('modelOverride'):
        unresolved.add('model_not_pinned')
    if run_meta is None:
        unresolved.add('launch_command_not_recorded')
    repository = repository_state(rubric, root)
    for skill, contract in rubric['contracts'].items():
        if repository['skillTrees'].get(skill) != contract['tree']:
            unresolved.add(f'rubric_contract_drift:{skill}')
    for c in aggregate['cases']:
        name = c['name']
        if name not in suite['cases']:
            unresolved.add(f'unknown_case:{name}')
            continue
        profile, case = suite['cases'][name], cases[name]
        ran_graders = c.get('graders') or case['graders']
        arms = {}
        for arm in ('with', 'without'):
            runs = c['arms'].get(arm)
            if runs is None:
                continue
            judged = []
            for i, run in enumerate(runs):
                copied = trace_dir / name / f'{arm}-{i}.jsonl' if trace_dir else None
                r = judge_run(name, profile, ran_graders, run, humans.get((name, arm, i)), rubric, status, judge_model, arm,
                              str(copied) if copied and copied.exists() else None)
                r['index'] = i
                judged.append(r)
            arms[arm] = {'runs': judged, 'summary': summarize(judged)}
        group = group_of(case, suite)
        if run_meta and run_meta.get('grants') != suite['groups'][group]['allowTools']:
            unresolved.add(f'grants_differ_from_suite:{group}')
        if 'without' in arms:
            comparison = {'noSkill': 'compared', 'nativeDeltaInformational': c['aggregates'].get('delta'),
                          'criteria': {cid: {arm: arms[arm]['summary']['criteria'].get(cid, {}) for arm in arms}
                                       for cid in profile['required']}}
        elif suite['groups'][group]['ablation'] == 'none':
            comparison = {'noSkill': 'n/a', 'reason': suite['groups'][group]['comparison']}
        else:
            comparison = {'noSkill': 'not_run', 'reason': 'run without the with-without ablation'}
        comparison['previousVersion'] = 'not_run'
        for arm in arms.values():
            if arm['summary']['excluded']:
                unresolved.add('excluded_runs')
            for r in arm['runs']:
                if r.get('provisional'):
                    unresolved.add('llm_graders_uncalibrated')
                if r['verdict'] in ('pending_human', 'required_pass'):
                    unresolved.add('human_review_pending')
        out_cases.append({'case': name, 'skill': profile['skill'], 'rubricCase': profile['rubricCase'],
                          'split': profile['split'], 'independentTask': profile['independentTask'],
                          'variantOf': profile.get('variantOf'), 'group': group,
                          'required': profile['required'], 'notApplicable': profile['notApplicable'],
                          'runsPerCase': c.get('runsPerCase'), 'arms': arms, 'comparison': comparison,
                          'nativeScoreInformational': c['aggregates'].get('score')})
    return {
        'recordVersion': 1,
        'rubricVersion': rubric['rubricVersion'],
        'goldStatus': rubric['goldStatus'],
        'run': {'claudeVersion': aggregate.get('claudeVersion'), 'startedAt': aggregate.get('startedAt'),
                'ablation': meta.get('ablation'), 'model': meta.get('modelOverride'), 'judgeModel': judge_model,
                'threshold': meta.get('threshold'), 'tagFilters': meta.get('tagFilters'),
                'plugins': meta.get('plugins'), 'partial': aggregate.get('partial'),
                'partialReason': aggregate.get('partialReason'), 'costUsd': aggregate.get('costUsd'),
                'launch': run_meta},
        'repository': repository,
        'cases': out_cases,
        'unresolved': sorted(unresolved),
    }


def calibration_cases(out_dir, suite_dir=SUITE_DIR):
    suite, rubric, cases = load(suite_dir)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob('cal-*'):
        shutil.rmtree(old)
    written = []
    for name, profile in suite['cases'].items():
        for item in profile.get('calibration', []):
            graders = []
            for g in cases[name]['graders']:
                if g['type'] not in ('regex', 'llm') or target_of(g) != item['target']:
                    continue
                if criterion_of(g['name'], rubric) not in item['expect']:
                    continue
                g = dict(g)
                if item['target'] == 'last_message':
                    g['target' if g['type'] == 'regex' else 'focus'] = {'source': 'file', 'path': LAST_MESSAGE_FILE}
                graders.append(g)
            if not any(g['type'] in PAID for g in graders):
                continue  # regex-only artifacts are already checked for free by deterministic_controls
            path = LAST_MESSAGE_FILE if item['target'] == 'last_message' else item['target']
            content = (suite_dir / item['artifact']).read_text()
            if ARTIFACT_DELIMITER in content:
                raise ValueError(f'{item["artifact"]} contains the heredoc delimiter')
            case_name = f'cal-{name}-{item["label"]}'
            case_dir = out_dir / case_name
            case_dir.mkdir()
            (case_dir / 'scaffold.sh').write_text(
                '#!/usr/bin/env bash\n# Generated by native_eval.py calibration-cases. Do not edit.\nset -euo pipefail\n'
                f'mkdir -p "$(dirname {path})"\ncat > {path} <<\'{ARTIFACT_DELIMITER}\'\n{content}'
                f'{"" if content.endswith(chr(10)) else chr(10)}{ARTIFACT_DELIMITER}\n')
            doc = {'schema_version': '1.1', 'name': case_name,
                   'description': f'Grader calibration for {name}, artifact {item["label"]} ({item["kind"]}).',
                   'tags': ['calibration'], 'runs': 1,
                   'execution': {'prompt': CALIBRATION_PROMPT, 'max_turns': 1, 'timeout_seconds': 120, 'allowed_tools': []},
                   'context': {'scaffold_script': 'scaffold.sh'}, 'graders': graders}
            (case_dir / 'case.yaml').write_text(json.dumps(doc, ensure_ascii=False, indent=2) + '\n')
            written.append(case_name)
    return written


JUDGE_SCHEMA = {'type': 'object', 'additionalProperties': False, 'required': ['verdict', 'reason'],
                'properties': {'verdict': {'type': 'string', 'enum': ['PASS', 'FAIL']}, 'reason': {'type': 'string'}}}
JUDGE_PROMPT = ('You are a strict evaluation judge. Decide whether the ARTIFACT satisfies the CRITERIA. '
                'Judge only from the text below; do not run commands or read files.\n\nCRITERIA:\n{criteria}\n\n'
                'ARTIFACT ({target}):\n<<<\n{artifact}\n>>>\n')


def codex_vote(criteria, target, artifact, model, effort):
    """One cross-provider judge vote through `codex exec`, isolated from user config, rules and session history."""
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / 'ws').mkdir()
        (tmp / 'schema.json').write_text(json.dumps(JUDGE_SCHEMA))
        cmd = ['codex', 'exec', '--ephemeral', '--ignore-user-config', '--ignore-rules', '--skip-git-repo-check',
               '-s', 'read-only', '-m', model, '-c', f'model_reasoning_effort="{effort}"',
               '--output-schema', str(tmp / 'schema.json'), '-o', str(tmp / 'out.json'), '-']
        prompt = JUDGE_PROMPT.format(criteria=criteria, target=target, artifact=artifact)
        for _ in range(2):
            subprocess.run(cmd, cwd=tmp / 'ws', input=prompt, capture_output=True, text=True, timeout=600)
            try:
                answer = json.loads((tmp / 'out.json').read_text())
                return answer['verdict'] == 'PASS', answer.get('reason', '')
            except (OSError, ValueError, KeyError):
                continue
    return None, 'judge produced no verdict'


def cross_judge_calibration(model, effort='high', votes=3, workers=6, repeats=1, case_glob='*', suite_dir=SUITE_DIR):
    """Judge the labelled artifacts with a Codex model and emit an aggregate-shaped result for `calibrate`."""
    from concurrent.futures import ThreadPoolExecutor
    from datetime import datetime, timezone
    suite, rubric, cases = load(suite_dir)
    jobs, regex_items, criteria_by = [], [], {}
    for name, profile in suite['cases'].items():
        for item in profile.get('calibration', []):
            graders = [g for g in cases[name]['graders'] if g['type'] in ('regex', 'llm')
                       and target_of(g) == item['target'] and criterion_of(g['name'], rubric) in item['expect']]
            if not any(g['type'] in PAID for g in graders):
                continue
            if not fnmatch.fnmatch(f'cal-{name}-{item["label"]}', case_glob):
                continue
            text = (suite_dir / item['artifact']).read_text()
            for g in graders:
                key = (f'cal-{name}-{item["label"]}', g['name'])
                if g['type'] == 'regex':
                    regex_items.append({'id': '|'.join(key), 'pattern': g['pattern'], 'flags': g.get('flags', ''),
                                        'match': g.get('match', 'contains'), 'text': text})
                else:
                    jobs += [((key[0], g['name'], r), g['criteria'], item['target'], text)
                             for r in range(repeats) for _ in range(votes)]
                    criteria_by[(key[0], g['name'])] = g['criteria']
    regex = run_node(regex_items) if regex_items else {}
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(lambda j: (j[0], codex_vote(j[1], j[2], j[3], model, effort)), jobs))
    votes_by = {}
    for (case_name, gname, rep), (vote, reason) in results:
        votes_by.setdefault(case_name, {}).setdefault(rep, {}).setdefault(gname, []).append((vote, reason))
    regex_by = {}
    for rid, r in regex.items():
        case_name, grader = rid.split('|')
        regex_by.setdefault(case_name, {})[grader] = r['matched']
    out_cases = []
    for case_name in sorted(set(votes_by) | set(regex_by)):
        runs, types = [], {}
        for rep in range(repeats):
            rows, error = [], None
            for gname, matched in regex_by.get(case_name, {}).items():
                rows.append({'name': gname, 'passed': matched, 'explanation': 'regex'})
                types[gname] = 'regex'
            for gname, value in votes_by.get(case_name, {}).get(rep, {}).items():
                valid = [v for v, _ in value if v is not None]
                if len(valid) * 2 <= len(value):
                    error = f'{gname}: judge produced no verdict'
                rows.append({'name': gname, 'passed': sum(valid) * 2 > len(value),
                             'judgeVotes': [v for v, _ in value], 'explanation': ' | '.join(r for _, r in value)})
                types[gname] = 'llm'
            runs.append({'error': error, 'skippedPaidGraders': False, 'graders': rows})
        out_cases.append({'name': case_name, 'graders': [{'name': n, 'type': ty, 'criteria': criteria_by.get((case_name, n))}
                                                         for n, ty in types.items()],
                          'arms': {'with': runs}})
    return {'schemaVersion': 1, 'claudeVersion': None, 'startedAt': datetime.now(timezone.utc).isoformat(),
            'partial': False, 'suite': {'judgeModel': f'codex:{model}:{effort}', 'ablation': 'none'}, 'cases': out_cases}


def calibrate(aggregate, suite_dir=SUITE_DIR):
    """Compare every calibration run with the expected verdicts; each run is one observation."""
    suite, rubric, _ = load(suite_dir)
    items = {f'cal-{name}-{item["label"]}': (name, item)
             for name, profile in suite['cases'].items() for item in profile.get('calibration', [])}
    rows, graders = [], {}
    for c in aggregate['cases']:
        if c['name'] not in items:
            continue
        name, item = items[c['name']]
        types = {g['name']: g['type'] for g in c['graders']}
        texts = {g['name']: g.get('graderMarkdown') or g.get('criteria') for g in c['graders']}
        for index, run in enumerate(c['arms'].get('with') or [None]):
            for cid, expected in item['expect'].items():
                results = [g for g in (run or {}).get('graders', []) if criterion_of(g['name'], rubric) == cid]
                if run is None or run.get('error') or not results:
                    observed = 'unknown'
                else:
                    observed = combine(['unknown' if types.get(g['name']) in PAID and run.get('skippedPaidGraders')
                                        else ('pass' if g['passed'] else 'fail') for g in results])
                if expected == 'human':
                    outcome = 'human_review'
                elif observed == 'unknown':
                    outcome = 'unjudged'
                elif observed == ('pass' if expected else 'fail'):
                    outcome = 'agree'
                else:
                    outcome = 'false_pass' if observed == 'pass' else 'false_fail'
                rows.append({'case': name, 'artifact': item['label'], 'kind': item['kind'], 'criterion': cid, 'run': index,
                             'expected': expected, 'observed': observed, 'outcome': outcome,
                             'graders': {g['name']: g['passed'] for g in results}})
                for g in results:
                    if types.get(g['name']) not in PAID:
                        continue
                    entry = graders.setdefault(f'{name}:{g["name"]}', {'agreed': 0, 'falsePass': 0, 'falseFail': 0, 'unjudged': 0, 'human': 0,
                                                                    'criteriaSha256': criteria_sha(texts.get(g['name']))})
                    key = {'agree': 'agreed', 'false_pass': 'falsePass', 'false_fail': 'falseFail',
                           'unjudged': 'unjudged', 'human_review': 'human'}[outcome]
                    entry[key] += 1
    summary = {k: sum(r['outcome'] == k for r in rows) for k in ('agree', 'false_pass', 'false_fail', 'unjudged', 'human_review')}
    summary['runs'] = len({(r['case'], r['artifact'], r['run']) for r in rows})
    return {'judgeModel': aggregate['suite'].get('judgeModel'), 'claudeVersion': aggregate.get('claudeVersion'),
            'startedAt': aggregate.get('startedAt'), 'rubricVersion': rubric['rubricVersion'],
            'summary': summary, 'rows': rows, 'graders': graders}


def redact(text):
    """Records are committed to a public repository: replace local absolute paths."""
    return text.replace(str(ROOT), '<repo>').replace(str(Path.home()), '~')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('check')
    sub.add_parser('plan')
    p = sub.add_parser('record')
    p.add_argument('aggregate')
    p.add_argument('--human')
    p.add_argument('--out')
    p = sub.add_parser('calibration-cases')
    p.add_argument('--out', default=str(ROOT / 'evals/claude-native-calibration'))
    p = sub.add_parser('calibrate')
    p.add_argument('aggregate')
    p.add_argument('--out')
    p = sub.add_parser('stage')
    p.add_argument('out')
    p.add_argument('--calibration', action='store_true')
    p = sub.add_parser('run', help='stage, run one group or the calibration suite, and record the command')
    p.add_argument('group')
    p.add_argument('--out', required=True)
    p.add_argument('--stage-dir', default=None)
    p.epilog = 'Options after a bare -- go to claude plugin eval, for example: -- --model M --judge-model J'
    p = sub.add_parser('cross-judge', help='judge the calibration artifacts with a Codex model')
    p.add_argument('--model', required=True)
    p.add_argument('--effort', default='high')
    p.add_argument('--votes', type=int, default=3)
    p.add_argument('--workers', type=int, default=6)
    p.add_argument('--repeats', type=int, default=1)
    p.add_argument('--case', default='*', help='glob over calibration case names, as with claude plugin eval --case')
    p.add_argument('--out', required=True)
    argv = list(sys.argv[1:] if argv is None else argv)
    extra = argv[argv.index('--') + 1:] if '--' in argv else []
    argv = argv[:argv.index('--')] if '--' in argv else argv
    args = parser.parse_args(argv)
    if args.command == 'stage':
        suite = load()[0]
        print(json.dumps(stage(args.out, [suite['calibrationDir'] if args.calibration else suite['evalDir']]), indent=2))
        return 0
    if args.command == 'run':
        import tempfile
        stage_dir = Path(args.stage_dir or tempfile.mkdtemp(prefix='paul-eval-')) / 'plugin'
        code, meta = run_group(args.group, args.out, stage_dir, extra)
        print(json.dumps({'exitCode': code, 'out': args.out, 'stage': meta['stage']['digest']}))
        return 0 if code in (0, 1, 2) else code
    if args.command == 'cross-judge':
        result = cross_judge_calibration(args.model, args.effort, args.votes, args.workers, args.repeats, args.case)
        Path(args.out).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        print(f'wrote {args.out}: {len(result["cases"])} calibration cases')
        return 0
    if args.command in ('check', 'plan'):
        problems = check_static() + deterministic_controls() if args.command == 'check' else plan()
        for problem in problems:
            print(problem, file=sys.stderr)
        print(f'{args.command}: {"ok" if not problems else f"{len(problems)} problem(s)"}')
        return 1 if problems else 0
    if args.command == 'calibration-cases':
        for name in calibration_cases(args.out):
            print(name)
        return 0
    aggregate = json.loads(Path(args.aggregate).read_text())
    meta_path = Path(args.aggregate + '.meta.json')
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else None
    traces = Path(args.aggregate + '.traces')
    result = (record(aggregate, args.human, meta=meta, trace_dir=traces if traces.is_dir() else None)
              if args.command == 'record' else calibrate(aggregate))
    text = redact(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    if args.out:
        Path(args.out).write_text(text)
    else:
        sys.stdout.write(text)
    if args.command == 'calibrate':
        print(json.dumps(result['summary']), file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
