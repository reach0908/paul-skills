"""Verify immutable evidence and execution facts separately from semantic judgments."""
from pathlib import Path
import hashlib, io, json, subprocess, tarfile
from collect import HERE, OWNERS

REPO = HERE.parents[1]
BASE = 'eb1977505c0a385a7608f19861962b660f575dfc'
OLD = 'evals/design-first-impression-2026-10-15'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def snapshot(path):
    return {str(p.relative_to(path)): sha(p.read_bytes())
            for p in sorted(path.rglob('*')) if p.is_file()}

def git_snapshot(*paths, revision=BASE):
    data = subprocess.check_output(['git', 'archive', revision, *paths], cwd=REPO)
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        return {m.name: sha(archive.extractfile(m).read()) for m in archive if m.isfile()}

def checked_response(receipt, root):
    path = root / receipt['response']
    assert path.resolve().is_relative_to(root.resolve()), 'Response path escaped evidence root'
    assert sha(path.read_bytes()) == receipt['response_sha256'], 'Response changed after collection'
    return receipt['response_sha256']

def owner_execution(receipt):
    calls = receipt['tool_calls']
    successes = [(i, c['input'].get('skill', '').split(':')[-1])
                 for i, c in enumerate(calls) if c['name'] == 'Skill'
                 and c['result_received'] and not c['is_error']
                 and c['input'].get('skill', '').split(':')[-1] in OWNERS]
    inspection = [i for i, c in enumerate(calls)
                  if c['name'] in ['Glob', 'Grep']
                  or (c['name'] == 'Read' and
                      (not c['input'].get('file_path', '').startswith('BUNDLE/')
                       or c['input'].get('file_path', '').endswith('/first-impression.md')))]
    ordered = [name for _, name in successes] == OWNERS
    before = ordered and (not inspection or successes[-1][0] < min(inspection))
    return {'successful_owner_calls': [name for _, name in successes],
            'all_six_in_order': ordered, 'before_artifact_and_optional_reference': before}

def check_review(receipt, review):
    assert receipt['response_sha256'] == review['response_sha256'], 'Semantic judgment is stale'
    assert review['status'] in ['reviewed', 'not_assessed']
    if not receipt['completed']:
        assert review['status'] == 'not_assessed', 'Incomplete trial counted as judged completion'
    if review['status'] == 'reviewed':
        assert review['evidence'] and review['criteria'], 'Missing review evidence'
        assert all(isinstance(v, bool) for v in review['criteria'].values())

def main():
    frozen = json.loads((HERE / 'freeze.json').read_text())
    for key, path in [('protocol', 'PROTOCOL.md'), ('cases', 'cases.json'), ('runner', 'run_trials.py')]:
        assert frozen[key] == sha((HERE / path).read_bytes()), f'Frozen {key} drift'
    assert frozen['base'] == BASE
    assert frozen['fixtures'] == snapshot(HERE / 'fixtures')
    assert frozen['arms']['baseline'] == git_snapshot('skills', '.claude-plugin')
    changes = {p for p in set(frozen['arms']['baseline']) | set(frozen['arms']['candidate'])
               if frozen['arms']['baseline'].get(p) != frozen['arms']['candidate'].get(p)}
    assert changes == {'skills/design/better-layout/first-impression.md',
                       'skills/design/better-interface/audit-procedure.md',
                       'skills/design/better-interface/review-format.md'}
    source = json.loads((HERE / 'candidate-source.json').read_text())
    assert frozen['arms']['candidate'] == git_snapshot('skills', '.claude-plugin', revision=source['commit']), 'Frozen candidate no longer matches its immutable source commit'
    old = git_snapshot(OLD)
    for path, digest in old.items():
        assert sha((REPO / path).read_bytes()) == digest, f'Old evidence changed: {path}'
    actual_old = {str(p.relative_to(REPO)) for p in (REPO / OLD).rglob('*')
                  if p.is_file() and '__pycache__' not in p.parts}
    assert actual_old == set(old), 'Old evidence file inventory changed'

    reviews = json.loads((HERE / 'manual-review.json').read_text())
    receipts = [json.loads(p.read_text()) for p in sorted((HERE / 'receipts').glob('*.json'))]
    key = lambda r: f"repair-{r['arm']}-{r['case_id']}"
    assert len({key(r) for r in receipts}) == len(receipts)
    assert set(reviews) == {key(r) for r in receipts}
    for r in receipts:
        checked_response(r, HERE)
        check_review(r, reviews[key(r)])
        assert r['freeze_sha256'] == sha((HERE / 'freeze.json').read_bytes())
        assert r['inputs_unchanged'] == (r['files_before'] == r['files_after'])
        if r['case_id'] in ['landing', 'warning', 'missing'] and reviews[key(r)]['status'] == 'reviewed':
            assert reviews[key(r)]['criteria']['owner_execution'] == owner_execution(r)['before_artifact_and_optional_reference']

    cases = json.loads((HERE / 'cases.json').read_text())
    stop = json.loads((HERE / 'stop.json').read_text()) if (HERE / 'stop.json').exists() else {}
    unstarted = stop.get('unstarted_cases', [])
    assert {r['case_id'] for r in receipts} == {c['id'] for c in cases} - set(unstarted)
    pairs = []
    for case in cases:
        if case['id'] in unstarted:
            continue
        pair = [r for r in receipts if r['case_id'] == case['id']]
        assert len(pair) == 2 and {r['arm'] for r in pair} == {'baseline', 'candidate'}
        assert pair[0]['prompt'] == pair[1]['prompt'] == case['prompt']
        assert pair[0]['files_before'] == pair[1]['files_before']
        prefix = case['fixture'] + '/'
        expected_input = {p[len(prefix):]: digest for p, digest in frozen['fixtures'].items() if p.startswith(prefix)}
        assert pair[0]['files_before'] == expected_input, 'Wrong fixture supplied to matched pair'
        matched = all(pair[0][f] == pair[1][f] for f in ['actual_model', 'host_version', 'requested_effort'])
        if matched and all(r['completed'] and r['inputs_unchanged'] and r['plugin_path_matches'] for r in pair):
            pairs.append(case['id'])

    reserved = sum(r['cost_usd'] if r['cost_usd'] is not None else 1.0 for r in receipts)
    assert reserved <= 16, 'Budget ceiling exceeded'
    before = json.loads((HERE / 'preservation-before.json').read_text())
    original = Path('/Users/jinhokim/dev/paul-skills')
    original_git = lambda *args: subprocess.check_output(['git', *args], cwd=original, text=True).strip()
    settings = Path.home() / '.claude/settings.json'
    after = {'original_head': original_git('rev-parse', 'HEAD'),
             'original_status': original_git('status', '--porcelain=v1'),
             'original_untracked': {p: sha((original / p).read_bytes())
                                    for p in original_git('ls-files', '--others', '--exclude-standard').splitlines()
                                    if (original / p).is_file()},
             'user_settings_sha256': sha(settings.read_bytes()) if settings.exists() else None,
             'previous_eval_tree': subprocess.check_output(['git', 'rev-parse', f'{BASE}:{OLD}'], cwd=REPO, text=True).strip()}
    assert before == after, 'Original checkout or user settings changed'
    result = {'integrity_pass': True, 'attempts': len(receipts), 'completed': sum(r['completed'] for r in receipts),
              'matched_completed_pairs': pairs, 'unstarted_cases': unstarted,
              'cost_with_timeout_reserves_usd': reserved, 'old_evidence_files_unchanged': len(old),
              'original_checkout_and_settings_unchanged': True,
              'owner_execution': {key(r): owner_execution(r) for r in receipts if r['case_id'] in ['landing', 'warning', 'missing']},
              'semantic_success_is_separate': True}
    (HERE / 'VERIFICATION.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
