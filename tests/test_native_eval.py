import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / 'evals/claude-native'
MODULE = SUITE / 'tools/native_eval.py'
spec = importlib.util.spec_from_file_location('native_eval', MODULE)
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)
HAS_NODE = shutil.which('node') is not None


def run_scaffold(script, workspace):
    """Run a fixture the way the eval runner does: empty cwd, temporary HOME, minimal environment."""
    home = workspace.parent
    env = {'PATH': os.environ['PATH'], 'HOME': str(home), 'TMPDIR': str(home), 'TERM': 'dumb', 'GIT_CONFIG_NOSYSTEM': '1'}
    subprocess.run(['bash', str(script)], cwd=workspace, env=env, check=True, capture_output=True)


def git(workspace, *args):
    return subprocess.run(['git', *args], cwd=workspace, check=True, capture_output=True, text=True).stdout


class TempSuite(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def copy_suite(self):
        target = self.root / 'suite'
        shutil.copytree(SUITE, target, ignore=shutil.ignore_patterns('results', '__pycache__'))
        return target

    def edit_json(self, path, change):
        data = json.loads(path.read_text())
        change(data)
        path.write_text(json.dumps(data, ensure_ascii=False))

    def workspace(self):
        ws = self.root / 'home/cwd'
        ws.mkdir(parents=True)
        return ws


class SuiteChecks(TempSuite):
    def test_suite_is_consistent(self):
        self.assertEqual(native.check_static(), [])

    @unittest.skipUnless(HAS_NODE, 'node is required for JavaScript regex semantics')
    def test_regex_and_input_controls_hold(self):
        self.assertEqual(native.deterministic_controls(), [])

    def test_ungraded_required_criterion_is_reported(self):
        suite = self.copy_suite()
        self.edit_json(suite / 'research-atlas-v2/case.yaml',
                       lambda d: d.update(graders=[g for g in d['graders'] if not g['name'].startswith('R4-')]))
        self.assertTrue(any('required R4 has no grader' in p for p in native.check_static(suite)))

    def test_unmapped_grader_name_is_reported(self):
        suite = self.copy_suite()
        self.edit_json(suite / 'user-flow-export-panel/case.yaml',
                       lambda d: d['graders'][0].update(name='flow-file-created'))
        self.assertTrue(any('must start with a rubric ID' in p for p in native.check_static(suite)))

    def test_silently_dropped_criterion_is_reported(self):
        suite = self.copy_suite()
        self.edit_json(suite / 'suite.json', lambda d: d['cases']['research-atlas-v2']['notApplicable'].pop('R6'))
        self.assertTrue(any('R6 must be required' in p for p in native.check_static(suite)))

    def test_grader_on_withheld_tool_is_reported(self):
        suite = self.copy_suite()
        self.edit_json(suite / 'research-atlas-v2/case.yaml', lambda d: d['graders'].append(
            {'name': 'C1-no-web-fetch', 'type': 'tool_used', 'tool': 'WebFetch', 'max': 0}))
        self.assertTrue(any('measures nothing' in p for p in native.check_static(suite)))

    def test_zero_call_grader_without_min_is_reported(self):
        # Observed in the first pilot: tool_used min defaults to 1, so max 0 alone can never pass.
        suite = self.copy_suite()
        self.edit_json(suite / 'research-atlas-v2/case.yaml', lambda d: next(
            g for g in d['graders'] if g['name'] == 'C4-no-eval-read').pop('min'))
        self.assertTrue(any('can never pass' in p for p in native.check_static(suite)))

    def test_diverging_shared_fixture_is_reported(self):
        suite = self.copy_suite()
        with (suite / 'interface-review-unnamed/scaffold.sh').open('a') as f:
            f.write('\ntouch extra\n')
        self.assertTrue(any('must stay identical' in p for p in native.check_static(suite)))

    @unittest.skipUnless(HAS_NODE, 'node is required for JavaScript regex semantics')
    def test_regex_that_fails_known_good_is_reported(self):
        suite = self.copy_suite()
        self.edit_json(suite / 'research-atlas-v2/case.yaml', lambda d: next(
            g for g in d['graders'] if g['name'] == 'R1-v2-limit-stated').update(pattern='30\\s?MB'))
        self.assertTrue(any('fails a known-good artifact' in p for p in native.deterministic_controls(suite)))

    @unittest.skipUnless(HAS_NODE, 'node is required for JavaScript regex semantics')
    def test_regex_only_criterion_that_passes_known_bad_is_reported(self):
        suite = self.copy_suite()
        self.edit_json(suite / 'interface-review-unnamed/case.yaml', lambda d: next(
            g for g in d['graders'] if g['name'] == 'I1-recommends-explicit-command').update(pattern='\\S'))
        self.assertTrue(any('all pass a known-bad artifact' in p for p in native.deterministic_controls(suite)))

    @unittest.skipUnless(HAS_NODE, 'node is required for JavaScript regex semantics')
    def test_wrong_input_match_is_reported(self):
        suite = self.copy_suite()
        self.edit_json(suite / 'interface-review-staged/case.yaml', lambda d: next(
            g for g in d['graders'] if g['name'] == 'I7-no-checkout-mutation').update(input_match='\\bgit\\b'))
        self.assertTrue(any('I7-no-checkout-mutation' in p for p in native.deterministic_controls(suite)))


class Fixtures(TempSuite):
    def test_interface_fixture_separates_index_from_working_tree(self):
        ws = self.workspace()
        run_scaffold(SUITE / 'interface-review-staged/scaffold.sh', ws)
        suite = json.loads((SUITE / 'suite.json').read_text())
        self.assertEqual(git(ws, 'rev-parse', 'HEAD').strip(),
                         suite['cases']['interface-review-staged']['fixture']['baseSha'])
        staged = git(ws, 'diff', '--cached', 'HEAD', '--', 'src/CloseControl.tsx')
        self.assertIn('+    <div className="close-control"', staged)
        self.assertIn('-    <button type="button"', staged)
        self.assertEqual(git(ws, 'diff', 'HEAD', '--', 'src/CloseControl.tsx'), '')
        self.assertIn('<div className="close-control"', git(ws, 'show', ':src/CloseControl.tsx'))
        self.assertIn('<button type="button"', (ws / 'src/CloseControl.tsx').read_text())
        self.assertEqual(sorted(git(ws, 'diff', '--cached', '--name-only', 'HEAD').split()),
                         ['pnpm-lock.yaml', 'src/CloseControl.tsx', 'src/LegacyCard.tsx'])
        legacy = git(ws, 'diff', '--cached', 'HEAD', '--', 'src/LegacyCard.tsx')
        self.assertIn(' ' * 5 + '<section className="legacy-card" style={{ width: 480 }}>', legacy)
        self.assertNotIn('+    <section', legacy)
        self.assertEqual(git(ws, 'ls-files', '--others', '--exclude-standard'), '')

    def test_research_fixture_supplies_the_four_sources(self):
        ws = self.workspace()
        run_scaffold(SUITE / 'research-atlas-v2/scaffold.sh', ws)
        sources = {p.name: p.read_text() for p in (ws / 'sources').iterdir()}
        self.assertEqual(sorted(sources), ['D1-atlas-import-v2-manual.md', 'D2-atlas-import-v1-manual.md',
                                           'D3-third-party-blog.md', 'D4-atlas-import-v2-release-notes.md'])
        self.assertIn('CSV files up to 20 MB are supported. XLSX is not supported.', sources['D1-atlas-import-v2-manual.md'])
        self.assertIn('The CSV limit increased from 5 MB to 20 MB.', sources['D4-atlas-import-v2-release-notes.md'])
        self.assertTrue((ws / 'outputs').is_dir() and not any((ws / 'outputs').iterdir()))


def research_run(fails=(), skipped=False, error=None, trace=None):
    case = json.loads((SUITE / 'research-atlas-v2/case.yaml').read_text())
    graders = [{'name': g['name'], 'passed': g['name'] not in fails, 'weight': 1, 'explanation': '',
                'withOnly': g['name'].startswith('IND-'), 'scored': not g['name'].startswith('IND-')}
               for g in case['graders']]
    return {'score': 0, 'passed': False, 'turns': 7, 'costUsd': 0.2, 'judgeCostUsd': 0.01, 'error': error,
            'tracePath': trace, 'skippedPaidGraders': skipped, 'graders': [] if error else graders}


def aggregate(name, with_runs, without_runs=None, ablation='with-without'):
    case = json.loads((SUITE / name / 'case.yaml').read_text())
    arms = {'with': with_runs}
    if without_runs is not None:
        arms['without'] = without_runs
    return {'schemaVersion': 1, 'claudeVersion': '2.1.301', 'startedAt': '2026-10-16T00:00:00Z', 'costUsd': 1.0,
            'partial': False, 'suite': {'root': str(ROOT), 'ablation': ablation, 'modelOverride': 'claude-sonnet-5-5',
                                        'judgeModel': 'claude-haiku-5-5', 'threshold': 1, 'plugins': []},
            'cases': [{'name': name, 'runsPerCase': len(with_runs),
                       'graders': [{'name': g['name'], 'type': g['type'], 'weight': 1, 'config': {}} for g in case['graders']],
                       'arms': arms, 'aggregates': {'score': 0.9, 'passRate': 0.5, 'delta': 0.2}}],
            'aggregates': {}}


class Records(TempSuite):
    def setUp(self):
        super().setUp()
        self.trace = self.root / 'saved-and-reread.jsonl'
        write_trace(self.trace, [('Write', {'file_path': '/w/outputs/research.md', 'content': 'x'}),
                                 ('Read', {'file_path': '/w/outputs/research.md'})])

    def run_ok(self, **kw):
        return research_run(trace=str(self.trace), **kw)

    def test_required_failure_is_not_offset_and_unjudged_stays_unknown(self):
        runs = [self.run_ok(), self.run_ok(fails={'R3-v1-limit-scoped'}), self.run_ok(skipped=True),
                self.run_ok(error='API error')]
        rec = native.record(aggregate('research-atlas-v2', runs, [self.run_ok(fails={'R2-owner-citations'})]))
        arm = rec['cases'][0]['arms']['with']
        verdicts = [r['verdict'] for r in arm['runs']]
        self.assertEqual(verdicts, ['pending_human', 'fail', 'undetermined', 'excluded'])
        self.assertEqual(arm['runs'][1]['criteria']['R3']['verdict'], 'fail')
        self.assertEqual(arm['runs'][2]['criteria']['R1']['verdict'], 'unknown')
        self.assertEqual(arm['runs'][2]['criteria']['C3']['verdict'], 'pass')
        self.assertEqual(arm['runs'][0]['criteria']['C1']['verdict'], 'pass')
        self.assertTrue(arm['runs'][0]['provisional'])
        self.assertEqual(arm['runs'][0]['indicators'], {'IND-research-skill-loaded': 'pass'})
        self.assertEqual(arm['summary']['excluded'], 1)
        self.assertIsNone(arm['summary']['cost']['tokens'])
        self.assertEqual(rec['cases'][0]['comparison']['noSkill'], 'compared')
        self.assertIn('llm_graders_uncalibrated', rec['unresolved'])
        self.assertIn('gold_not_human_confirmed', rec['unresolved'])

    def test_human_review_completes_a_run(self):
        review = self.root / 'human.json'
        review.write_text(json.dumps({'reviewer': 'maintainer', 'reviews': [
            {'case': 'research-atlas-v2', 'arm': 'with', 'run': 0, 'criteria': {'C2': 'pass'},
             'quality': {'RQ1': 'usable', 'RQ2': 'minor_edit'}, 'taskStatus': 'complete'},
            {'case': 'research-atlas-v2', 'arm': 'with', 'run': 1, 'criteria': {'C2': 'pass'},
             'quality': {'RQ1': 'rewrite', 'RQ2': 'usable'}, 'taskStatus': 'complete'}]}))
        rec = native.record(aggregate('research-atlas-v2', [self.run_ok(), self.run_ok()]), str(review))
        runs = rec['cases'][0]['arms']['with']['runs']
        self.assertEqual([r['verdict'] for r in runs], ['pass', 'quality_hold'])
        self.assertEqual(runs[0]['reviewer'], 'maintainer')
        self.assertEqual(runs[0]['taskStatus'], 'complete')

    def test_human_failure_overrides_passing_graders(self):
        review = self.root / 'human.json'
        review.write_text(json.dumps({'reviews': [
            {'case': 'research-atlas-v2', 'arm': 'with', 'run': 0, 'criteria': {'R2': 'fail', 'C2': 'pass'}}]}))
        rec = native.record(aggregate('research-atlas-v2', [self.run_ok()]), str(review))
        run = rec['cases'][0]['arms']['with']['runs'][0]
        self.assertEqual((run['criteria']['R2']['verdict'], run['verdict']), ('fail', 'fail'))

    def test_plugin_only_criteria_are_not_applicable_in_the_no_plugin_arm(self):
        case = json.loads((SUITE / 'better-interface-settings-audit/case.yaml').read_text())
        def run(passed):
            return {'score': 0, 'turns': 4, 'costUsd': 0.1, 'judgeCostUsd': 0.01, 'error': None, 'skippedPaidGraders': False,
                    'graders': [{'name': g['name'], 'passed': passed(g['name']), 'weight': 1, 'explanation': ''} for g in case['graders']]}
        without = run(lambda n: not n.startswith(('A1-', 'A2-')))
        rec = native.record(aggregate('better-interface-settings-audit', [run(lambda n: True)], [without]))
        arm = rec['cases'][0]['arms']['without']['runs'][0]
        self.assertEqual(arm['criteria']['A1']['verdict'], 'n/a')
        self.assertEqual(arm['criteria']['A2']['verdict'], 'n/a')
        self.assertEqual(arm['verdict'], 'required_pass')

    def test_calibration_is_tied_to_the_judge_and_the_exact_criteria(self):
        text = 'PASS only if the report is good.'
        status = {'judgeModel': 'claude-opus-5-5', 'graders': {'research-atlas-v2:R4-no-invented-speed': {
            'agreed': 3, 'falsePass': 0, 'falseFail': 0, 'criteriaSha256': native.criteria_sha(text)}}}
        ok = lambda judge, criteria: native.calibrated(status, 'research-atlas-v2', 'R4-no-invented-speed', judge, criteria)
        self.assertTrue(ok('claude-opus-5-5', text))
        self.assertFalse(ok('claude-opus-5-5', text + ' Edited.'))
        self.assertFalse(ok('claude-haiku-5-5', text))
        old = 'PASS only if the earlier report is good.'
        status['graders']['research-atlas-v2:R4-no-invented-speed@' + native.criteria_sha(old)] = {
            'agreed': 3, 'falsePass': 0, 'falseFail': 0, 'criteriaSha256': native.criteria_sha(old)}
        self.assertTrue(ok('claude-opus-5-5', old))
        del status['graders']['research-atlas-v2:R4-no-invented-speed']['criteriaSha256']
        self.assertFalse(ok('claude-opus-5-5', text))

    def test_skill_changed_since_rubric_is_flagged(self):
        self.assertFalse(any(u.startswith('rubric_contract_drift')
                             for u in native.record(aggregate('research-atlas-v2', [research_run()]))['unresolved']))
        suite = self.copy_suite()
        self.edit_json(suite / 'rubric.json', lambda d: d['contracts']['research'].update(tree='0' * 40))
        rec = native.record(aggregate('research-atlas-v2', [research_run()]), suite_dir=suite)
        self.assertIn('rubric_contract_drift:research', rec['unresolved'])

    def test_single_arm_group_reports_no_skill_comparison_as_not_applicable(self):
        case = json.loads((SUITE / 'interface-review-unnamed/case.yaml').read_text())
        run = {'score': 1, 'turns': 2, 'costUsd': 0.05, 'judgeCostUsd': 0, 'error': None, 'skippedPaidGraders': False,
               'graders': [{'name': g['name'], 'passed': True, 'weight': 1, 'explanation': ''} for g in case['graders']]}
        rec = native.record(aggregate('interface-review-unnamed', [run], ablation='none'))
        case_rec = rec['cases'][0]
        self.assertEqual(case_rec['comparison']['noSkill'], 'n/a')
        self.assertEqual(case_rec['arms']['with']['runs'][0]['verdict'], 'pending_human')
        self.assertEqual(case_rec['arms']['with']['runs'][0]['criteria']['I1']['verdict'], 'pass')
        self.assertEqual(case_rec['arms']['with']['runs'][0]['criteria']['C2']['verdict'], 'pending_human')


def write_trace(path, calls):
    lines = [json.dumps({'type': 'assistant', 'message': {'content': [
        {'type': 'tool_use', 'name': name, 'input': inp}]}}) for name, inp in calls]
    path.write_text('\n'.join(lines) + '\n')


class TraceChecks(TempSuite):
    # Observed in the second pilot: Write used under an Edit grant, and an import line inside a
    # test edit matched a source-path pattern that searched the whole JSON input.
    def profile(self, name):
        return json.loads((SUITE / 'suite.json').read_text())['cases'][name]

    def test_import_text_does_not_count_as_a_source_change(self):
        trace = self.root / 't.jsonl'
        write_trace(trace, [
            ('Edit', {'file_path': '/w/test/onboarding.test.js', 'old_string': "from '../src/onboarding.js'", 'new_string': 'x'}),
            ('Bash', {'command': 'npm test'}),
            ('Edit', {'file_path': '/w/src/onboarding.js', 'old_string': 'scrollTop: 0, ', 'new_string': ''})])
        rows = {r['name']: r['value'] for r in native.trace_rows(self.profile('diagnosing-bugs-scroll-reset'), {}, str(trace))}
        self.assertEqual(rows, {'C3-source-changed': 'pass', 'G1-loop-run-before-fix': 'pass', 'G1-test-written-before-fix': 'pass'})

    def test_fix_before_test_fails_the_order(self):
        trace = self.root / 't.jsonl'
        write_trace(trace, [
            ('Write', {'file_path': '/w/src/onboarding.js', 'content': 'x'}),
            ('Edit', {'file_path': '/w/test/onboarding.test.js', 'old_string': 'a', 'new_string': 'b'}),
            ('Bash', {'command': 'node --test'})])
        rows = {r['name']: r['value'] for r in native.trace_rows(self.profile('diagnosing-bugs-scroll-reset'), {}, str(trace))}
        self.assertEqual(rows['C3-source-changed'], 'pass')
        self.assertEqual(rows['G1-loop-run-before-fix'], 'fail')
        self.assertEqual(rows['G1-test-written-before-fix'], 'fail')

    def test_write_counts_as_a_card_change(self):
        trace = self.root / 't.jsonl'
        calls = [('Read', {'file_path': '/w/docs/decisions.md'}), ('Read', {'file_path': '/w/src/TripFolder.tsx'}),
                 ('Write', {'file_path': '/w/src/TripCard.tsx', 'content': 'x'})]
        write_trace(trace, [('Skill', {'skill': 'paul-skills:build-design'})] + calls)
        rows = {r['name']: r['value'] for r in native.trace_rows(self.profile('build-design-scoped-card'), {}, str(trace))}
        self.assertEqual(set(rows.values()), {'pass'})
        write_trace(trace, calls)
        rows = {r['name']: r['value'] for r in native.trace_rows(self.profile('build-design-scoped-card'), {}, str(trace))}
        self.assertEqual(rows['B5-skill-loaded'], 'fail')

    def test_near_miss_fails_when_the_skill_loads(self):
        trace = self.root / 't.jsonl'
        write_trace(trace, [('Skill', {'skill': 'paul-skills:code-review'}), ('Read', {'file_path': '/w/src/discount.js'})])
        rows = {r['name']: r['value'] for r in native.trace_rows(self.profile('code-review-near-miss'), {}, str(trace))}
        self.assertEqual(rows['K5-skill-not-loaded'], 'fail')
        write_trace(trace, [('Read', {'file_path': '/w/src/discount.js'})])
        rows = {r['name']: r['value'] for r in native.trace_rows(self.profile('code-review-near-miss'), {}, str(trace))}
        self.assertEqual(rows['K5-skill-not-loaded'], 'pass')

    def test_reread_may_follow_an_existence_check(self):
        trace = self.root / 't.jsonl'
        check = self.profile('research-atlas-v2')
        write_trace(trace, [('Read', {'file_path': '/w/outputs/research.md'}), ('Write', {'file_path': '/w/outputs/research.md', 'content': 'x'})])
        self.assertEqual(native.trace_rows(check, {}, str(trace))[0]['value'], 'fail')
        write_trace(trace, [('Read', {'file_path': '/w/outputs/research.md'}), ('Write', {'file_path': '/w/outputs/research.md', 'content': 'x'}),
                            ('Read', {'file_path': '/w/outputs/research.md'})])
        self.assertEqual(native.trace_rows(check, {}, str(trace))[0]['value'], 'pass')

    def test_missing_trace_is_unknown_not_fail(self):
        rows = native.trace_rows(self.profile('research-atlas-v2'), {'tracePath': str(self.root / 'absent.jsonl')})
        self.assertEqual([r['value'] for r in rows], ['unknown'])

    def test_positive_file_change_grader_is_rejected(self):
        suite = self.copy_suite()
        self.edit_json(suite / 'build-design-scoped-card/case.yaml', lambda d: d['graders'].append(
            {'name': 'C3-card-edited', 'type': 'tool_used', 'tool': 'Edit', 'input_match': '"file_path"\\s*:\\s*"[^"]*TripCard', 'min': 1}))
        self.assertTrue(any('use traceChecks' in p for p in native.check_static(suite)))

    def test_unpaired_zero_call_file_grader_is_rejected(self):
        suite = self.copy_suite()
        self.edit_json(suite / 'research-atlas-v2/case.yaml', lambda d: d.update(
            graders=[g for g in d['graders'] if g['name'] != 'C1-no-other-edit']))
        self.assertTrue(any('has no matching Edit grader' in p for p in native.check_static(suite)))

    def test_llm_grader_without_a_fail_artifact_is_rejected(self):
        suite = self.copy_suite()
        self.edit_json(suite / 'suite.json', lambda d: d['cases']['build-design-scoped-card'].update(
            calibration=[c for c in d['cases']['build-design-scoped-card']['calibration'] if c['label'] != 'B-F-css']))
        self.assertTrue(any('B3-photo-first-styles needs a pass and a fail' in p for p in native.check_static(suite)))


class Staging(TempSuite):
    def test_stage_copies_only_manifest_skills_and_the_eval_dir(self):
        out = self.root / 'stage'
        marker = native.stage(out, ['evals/claude-native'])
        manifest = json.loads((ROOT / '.claude-plugin/plugin.json').read_text())
        self.assertTrue((out / '.claude-plugin/plugin.json').is_file())
        self.assertTrue(all((out / p[2:] / 'SKILL.md').is_file() for p in manifest['skills']))
        self.assertTrue((out / 'evals/claude-native/suite.json').is_file())
        self.assertFalse((out / 'skills/in-progress').exists())
        self.assertFalse((out / 'evals/design-beta').exists())
        self.assertFalse((out / 'node_modules').exists())
        self.assertTrue(marker['digest'].startswith('sha256:'))
        self.assertLess(marker['fileCount'], 20000)

    def test_stage_refuses_to_replace_an_ordinary_directory(self):
        out = self.root / 'precious'
        out.mkdir()
        (out / 'notes.txt').write_text('keep')
        with self.assertRaises(ValueError):
            native.stage(out, ['evals/claude-native'])
        self.assertEqual((out / 'notes.txt').read_text(), 'keep')

    def test_record_flags_grants_that_differ_from_the_suite(self):
        meta = {'group': 'group-with-without', 'grants': ['Write', 'Bash']}
        rec = native.record(aggregate('research-atlas-v2', [research_run()]), meta=meta)
        self.assertIn('grants_differ_from_suite:group-with-without', rec['unresolved'])
        self.assertNotIn('launch_command_not_recorded', rec['unresolved'])


class Calibration(TempSuite):
    @unittest.skipUnless(HAS_NODE, 'node is required for JavaScript regex semantics')
    def test_cross_judge_majority_feeds_calibrate(self):
        def fake_vote(criteria, target, artifact, model, effort):
            # A judge that passes everything: every known-bad artifact becomes a false pass.
            return True, 'looks fine'
        original = native.codex_vote
        native.codex_vote = fake_vote
        try:
            agg = native.cross_judge_calibration('fake-model', votes=3, workers=2)
        finally:
            native.codex_vote = original
        self.assertEqual(agg['suite']['judgeModel'], 'codex:fake-model:high')
        result = native.calibrate(agg)
        outcomes = {(r['artifact'], r['criterion']): r['outcome'] for r in result['rows']}
        self.assertEqual(outcomes[('U-F', 'U4')], 'false_pass')
        self.assertEqual(outcomes[('R-P', 'R2')], 'agree')
        self.assertEqual(outcomes[('R-B', 'R2')], 'human_review')
        self.assertNotIn(('I-N-P', 'I1'), outcomes)

    def test_generated_cases_reproduce_artifacts_and_rewrite_last_message_targets(self):
        out = self.root / 'calibration'
        names = native.calibration_cases(out)
        self.assertIn('cal-interface-review-staged-I-P', names)
        self.assertNotIn('cal-interface-review-unnamed-I-N-P', names)
        doc = json.loads((out / 'cal-interface-review-staged-I-P/case.yaml').read_text())
        self.assertTrue(all((g.get('target') or g.get('focus')) == {'source': 'file', 'path': native.LAST_MESSAGE_FILE}
                            for g in doc['graders']))
        self.assertEqual(doc['execution']['allowed_tools'], [])
        ws = self.workspace()
        run_scaffold(out / 'cal-interface-review-staged-I-P/scaffold.sh', ws)
        self.assertEqual((ws / native.LAST_MESSAGE_FILE).read_bytes(),
                         (SUITE / 'calibration/interface-review-staged/I-P.md').read_bytes())

    def test_calibration_counts_false_pass_separately(self):
        out = self.root / 'calibration'
        native.calibration_cases(out)
        doc = json.loads((out / 'cal-user-flow-export-panel-U-B/case.yaml').read_text())
        run = {'error': None, 'skippedPaidGraders': False,
               'graders': [{'name': g['name'], 'passed': True} for g in doc['graders']]}
        agg = {'claudeVersion': '2.1.301', 'suite': {'judgeModel': 'claude-haiku-5-5'},
               'cases': [{'name': 'cal-user-flow-export-panel-U-B', 'graders': doc['graders'], 'arms': {'with': [run]}}]}
        result = native.calibrate(agg)
        outcomes = {r['criterion']: r['outcome'] for r in result['rows']}
        self.assertEqual(outcomes['U4'], 'false_pass')
        self.assertEqual(outcomes['U5'], 'false_pass')
        self.assertEqual(outcomes['U1'], 'agree')
        self.assertEqual(result['graders']['user-flow-export-panel:U4-close-and-reopen-consistent']['falsePass'], 1)


if __name__ == '__main__':
    unittest.main()
