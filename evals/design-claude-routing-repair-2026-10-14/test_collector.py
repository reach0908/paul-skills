"""Negative controls for invocation evidence, independent of paid model trials."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import collect


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = '---\nname: owner\n---\n\n# Owner\n\nComplete body.\n'
        skill = self.root / 'skills/design/owner'
        skill.mkdir(parents=True)
        (skill / 'SKILL.md').write_text(self.source)
        self.patch = patch.multiple(collect, RAW=self.root, CACHE=self.root,
                                   NAMES={'owner'}, AUTO={'owner'}, USER_ONLY=set())
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.case = {'id': 'case', 'mode': 'implicit', 'expected': 'owner', 'prompt': 'Prepare the task.'}
        self.meta = {'exit_code': 0, 'timed_out': False, 'files_before': {}, 'files_after': {},
                     'cwd': '/trial', 'session_id': 'test', 'started_at': '2026-10-14',
                     'duration_seconds': 1, 'protocol_sha256': 'p', 'cases_sha256': 'c'}
        self.stream = [
            {'type': 'system', 'subtype': 'init', 'session_id': 'test', 'slash_commands': ['paul-skills:owner'],
             'plugins': [{'name': 'paul-skills', 'version': '0.4.0', 'path': str(self.root)}]},
            {'type': 'result', 'subtype': 'success', 'session_id': 'test', 'result': 'Used owner.', 'permission_denials': []}]
        self.trace = [
            {'type': 'attachment', 'attachment': {'type': 'skill_listing', 'isInitial': True,
                                                'names': ['paul-skills:owner']}},
            {'type': 'assistant', 'message': {'content': [
                {'type': 'tool_use', 'name': 'Skill', 'id': 'call1', 'input': {'skill': 'paul-skills:owner'}}]}},
            {'type': 'user', 'message': {'content': [
                {'type': 'tool_result', 'tool_use_id': 'call1', 'content': 'Launching skill'}]}},
            {'type': 'user', 'message': {'content': [
                {'type': 'text', 'text': f'Base directory for this skill: {skill}\n\n# Owner\n\nComplete body.'}]}}
        ]

    def evaluate(self):
        (self.root / 'case.meta.json').write_text(json.dumps(self.meta))
        for name, data in [('case.jsonl', self.stream), ('case.transcript.jsonl', self.trace)]:
            (self.root / name).write_text('\n'.join(json.dumps(e) for e in data))
        return collect.collect_case(self.case)

    def test_real_call_and_full_body_pass(self):
        self.assertTrue(self.evaluate()['pass'])

    def test_final_name_claim_without_body_fails(self):
        self.trace.pop()
        self.assertFalse(self.evaluate()['pass'])

    def test_body_without_successful_implicit_call_fails(self):
        self.trace = [self.trace[0], self.trace[3]]
        self.assertFalse(self.evaluate()['pass'])

    def test_denied_call_is_not_success(self):
        self.trace[2]['message']['content'][0]['is_error'] = True
        self.assertFalse(self.evaluate()['pass'])

    def test_truncated_body_fails(self):
        self.trace[3]['message']['content'][0]['text'] = 'Base directory for this skill: /skill\n\n# Owner'
        self.assertFalse(self.evaluate()['pass'])

    def test_assistant_quoted_body_is_not_host_load(self):
        self.trace[3]['type'] = 'assistant'
        self.assertFalse(self.evaluate()['pass'])

    def test_init_inventory_does_not_replace_model_catalog(self):
        self.stream[0]['skills'] = ['paul-skills:owner']
        self.trace.pop(0)
        self.assertFalse(self.evaluate()['pass'])

    def test_explicit_expansion_needs_no_skill_tool_call(self):
        self.case['mode'] = 'explicit'
        self.trace = [self.trace[0], self.trace[3]]
        self.assertTrue(self.evaluate()['pass'])

    def test_incomplete_process_fails_despite_body(self):
        self.meta['timed_out'] = True
        self.assertFalse(self.evaluate()['pass'])

    def hidden_setup(self):
        collect.NAMES.add('hidden')
        collect.USER_ONLY.add('hidden')
        skill = self.root / 'skills/design/hidden'
        skill.mkdir(parents=True)
        (skill / 'SKILL.md').write_text('---\nname: hidden\n---\n\n# Hidden\nSecret workflow.\n')
        self.stream[0]['slash_commands'].append('paul-skills:hidden')

    def test_user_only_exposure_fails(self):
        self.hidden_setup()
        self.trace[0]['attachment']['names'].append('paul-skills:hidden')
        self.assertFalse(self.evaluate()['checks']['automatic_catalog_exact_12'])

    def test_user_only_relative_read_attempt_fails(self):
        self.hidden_setup()
        self.trace.append({'type': 'assistant', 'message': {'content': [
            {'type': 'tool_use', 'name': 'Read', 'id': 'call2',
             'input': {'file_path': 'hidden/SKILL.md'}}]}})
        self.assertFalse(self.evaluate()['checks']['no_user_only_loads_or_attempts'])

    def test_user_only_body_in_broad_file_read_fails(self):
        self.hidden_setup()
        self.trace.append({'type': 'user', 'message': {'content': [
            {'type': 'tool_result', 'tool_use_id': 'call2',
             'content': '     1→# Hidden\n     2→Secret workflow.'}]}})
        self.assertFalse(self.evaluate()['checks']['no_user_only_loads_or_attempts'])

    def test_changed_inputs_fail(self):
        self.meta['files_after'] = {'unexpected.html': 'digest'}
        self.assertFalse(self.evaluate()['pass'])

    def test_wrong_plugin_path_fails(self):
        self.stream[0]['plugins'][0]['path'] = '/different/install'
        self.assertFalse(self.evaluate()['checks']['correct_plugin_source'])

    def routing_setup(self, target='staged'):
        self.case.update(mode='boundary', forbidden='interface-review', target=target)
        self.stream[1]['result'] = '/paul-skills:interface-review' + (' ' + target if target else '')

    def test_routing_preserves_staged_target(self):
        self.routing_setup()
        self.assertTrue(self.evaluate()['pass'])
        self.stream[1]['result'] = '/paul-skills:interface-review working'
        self.assertFalse(self.evaluate()['checks']['explicit_handoff'])

    def test_routing_file_discovery_fails(self):
        self.routing_setup()
        self.trace.append({'type': 'assistant', 'message': {'content': [
            {'type': 'tool_use', 'name': 'Glob', 'id': 'call2', 'input': {'pattern': '**/*'}}]}})
        self.assertFalse(self.evaluate()['checks']['no_file_inspection'])

    def test_explicit_router_needs_no_skill_call(self):
        self.routing_setup()
        self.case['entry'] = 'explicit'
        self.trace = [self.trace[0], self.trace[3]]
        self.assertTrue(self.evaluate()['pass'])

    def test_unspecified_target_cannot_be_invented(self):
        self.routing_setup('')
        self.assertTrue(self.evaluate()['pass'])
        self.stream[1]['result'] += ' working'
        self.assertFalse(self.evaluate()['checks']['no_invented_target'])

    def test_optional_examples_do_not_change_unspecified_primary_target(self):
        self.routing_setup('')
        self.stream[1]['result'] += '\nOptional targets: `/paul-skills:interface-review staged`'
        self.assertTrue(self.evaluate()['checks']['no_invented_target'])

    def test_handoff_requires_domain_owners_and_git_evidence(self):
        self.case['mode'] = 'handoff'
        row = self.evaluate()
        self.assertFalse(row['checks']['authorized_owners_loaded'])
        self.assertFalse(row['checks']['real_git_diff'])
        self.assertFalse(row['checks']['classified_regression'])


if __name__ == '__main__':
    unittest.main()
