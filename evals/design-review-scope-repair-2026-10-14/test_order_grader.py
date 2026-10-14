"""Controls for the observed batched-read and pre-routing inspection failure."""
import unittest
from pathlib import Path
from collect_codex import permitted_route_command, exact_body_observed, source_path_observed
class RouteOrderControls(unittest.TestCase):
    def setUp(self):
        self.plugin=Path('/trial/plugin')
        self.router=str(self.plugin/'skills/design/better-interface/SKILL.md')
    def test_router_read(self):
        self.assertTrue(permitted_route_command('cat '+self.router,self.plugin,{'better-interface'}))
    def test_chained_status_cannot_hide_behind_router_path(self):
        self.assertFalse(permitted_route_command('git status --short && cat '+self.router,self.plugin,{'better-interface'}))
    def test_diff_stat_counts_as_inspection(self):
        self.assertFalse(permitted_route_command('cat '+self.router+' && git diff --cached --stat',self.plugin,{'better-interface'}))
    def test_repository_discovery_counts(self):
        self.assertFalse(permitted_route_command('rg --files && cat '+self.router,self.plugin,{'better-interface'}))
    def test_partial_domain_read_cannot_hide_in_router_command(self):
        command='cat '+self.router+' && head -n 8 /trial/plugin/skills/design/better-layout/SKILL.md'
        self.assertFalse(permitted_route_command(command,self.plugin,{'better-interface'}))
    def test_context_memory_is_allowed(self):
        self.assertTrue(permitted_route_command('cat /trial/memories/MEMORY.md',self.plugin,{'better-interface'}))
    def test_memory_cannot_mask_status(self):
        self.assertFalse(permitted_route_command('cat /trial/memories/MEMORY.md && git status --short',self.plugin,{'better-interface'}))
    def test_generic_domain_read_is_not_route(self):
        self.assertFalse(permitted_route_command('cat /trial/plugin/skills/design/better-layout/SKILL.md',self.plugin,{'better-interface'}))
    def test_explicit_domain_may_be_injected_or_read(self):
        self.assertTrue(permitted_route_command('cat /trial/plugin/skills/design/better-layout/SKILL.md',self.plugin,{'better-interface','better-layout'}))
    def test_execution_procedure_is_not_entry(self):
        self.assertFalse(permitted_route_command('cat '+self.router+' && cat /trial/plugin/skills/design/better-interface/audit-procedure.md',self.plugin,{'better-interface'}))
class SourceReadControls(unittest.TestCase):
    def test_diff_prefix_is_decoded_exactly(self):
        self.assertTrue(exact_body_observed({'command':'git diff --no-index /dev/null /skill','aggregated_output':'diff --git a b\n+++ b\n+one\n+two\n'},'one\ntwo'))
    def test_diff_option_separator_is_supported(self):
        self.assertTrue(exact_body_observed({'command':'git diff --no-index -- /dev/null /skill','aggregated_output':'diff --git a b\n+++ b\n+one\n+two\n'},'one\ntwo'))
    def test_partial_diff_is_not_full_body(self):
        self.assertFalse(exact_body_observed({'command':'git diff --no-index /dev/null /skill','aggregated_output':'+one\n'},'one\ntwo'))
    def test_relative_read_needs_matching_cwd_and_body(self):
        path=Path('/trial/plugin/skills/design/better-colors/SKILL.md')
        trace=[{'payload':{'type':'custom_tool_call','input':"tools.exec_command({cmd: 'cat SKILL.md', workdir: '/trial/plugin/skills/design/better-colors'})"}}]
        commands=[{'command':'cat SKILL.md','aggregated_output':'complete body'}]
        self.assertTrue(source_path_observed(commands,trace,path,'complete body'))
        self.assertFalse(source_path_observed(commands,trace,Path('/wrong/SKILL.md'),'complete body'))
        self.assertFalse(source_path_observed(commands,trace,path,'different body'))
class ScopeControls(unittest.TestCase):
    def test_working_requires_head_and_untracked_inventory(self):
        from scope_checks import local_scope_checks
        case={'mode':'handoff','id':'working-divergent'}
        good=['git diff HEAD','git ls-files --others --exclude-standard']
        self.assertTrue(all(local_scope_checks(case,good).values()))
        self.assertFalse(local_scope_checks(case,good[:1])['target_snapshot_read'])
        self.assertFalse(local_scope_checks(case,good+['git merge-base main HEAD'])['no_default_branch_resolution'])
    def test_staged_requires_index_content_not_working_copy(self):
        from scope_checks import local_scope_checks
        case={'mode':'handoff','id':'staged-divergent'}
        good=['git diff --cached HEAD','git show :src/Panel.html']
        self.assertTrue(all(local_scope_checks(case,good).values()))
        self.assertFalse(local_scope_checks(case,['git diff HEAD','cat src/Panel.html'])['target_snapshot_read'])
        self.assertFalse(local_scope_checks(case,good+['git symbolic-ref refs/remotes/origin/HEAD'])['no_default_branch_resolution'])
class NativeTraceControls(unittest.TestCase):
    def test_requires_matching_call_path_and_full_body(self):
        from collect_codex import trace_read_evidence
        path=Path('/trial/source/SKILL.md')
        trace=[{'payload':{'type':'custom_tool_call','call_id':'one','input':'cat '+str(path)}},{'payload':{'type':'custom_tool_call_output','call_id':'one','output':[{'type':'input_text','text':'exact complete body'}]}}]
        self.assertIsNotNone(trace_read_evidence(trace,path,'exact complete body'))
        self.assertIsNone(trace_read_evidence(trace,Path('/other/SKILL.md'),'exact complete body'))
        self.assertIsNone(trace_read_evidence(trace,path,'exact complete body plus missing tail'))
        trace[1]['payload']['call_id']='unrelated'
        self.assertIsNone(trace_read_evidence(trace,path,'exact complete body'))
class ExitControls(unittest.TestCase):
    def test_no_match_is_not_read_error(self):
        from collect_codex import command_succeeded
        self.assertTrue(command_succeeded({'command':'rg -n missing /trial/memories/MEMORY.md','exit_code':1,'aggregated_output':''}))
        self.assertFalse(command_succeeded({'command':'sed -n 1,240p ""','exit_code':1,'aggregated_output':'sed: : No such file or directory'}))
        self.assertFalse(command_succeeded({'command':'rg --bad-option file','exit_code':2,'aggregated_output':'error'}))
        self.assertFalse(command_succeeded({'command':'false && rg pattern /trial/memories/MEMORY.md','exit_code':1,'aggregated_output':''}))
class NumberedReadControls(unittest.TestCase):
    def test_claude_line_prefix_preserves_blank_lines_and_indentation(self):
        from collect_claude import strip_line_numbers
        source='# Title\n\n    code\n'
        numbered='1\t# Title\n2\t\n3\t    code\n'
        self.assertEqual(strip_line_numbers(numbered),source)
if __name__=='__main__':unittest.main()
