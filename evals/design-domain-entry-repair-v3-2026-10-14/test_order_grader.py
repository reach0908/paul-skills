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
    def test_other_skill_cannot_hide_in_router_command(self):
        self.assertFalse(permitted_route_command('cat '+self.router+' && cat /trial/plugin/skills/engineering/code-review/SKILL.md',self.plugin,{'better-interface'}))
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
        quoted=[{'payload':{'type':'custom_tool_call','input':'''tools.exec_command({cmd: 'cat SKILL.md', "workdir": '/trial/plugin/skills/design/better-colors'})'''}}]
        self.assertTrue(source_path_observed(commands,quoted,path,'complete body'))
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
class ReferenceReadControls(unittest.TestCase):
    def test_relative_reference_needs_call_cwd_and_full_body(self):
        from collect_references import relative_reference_evidence
        p=Path('/trial/plugin/contrast.md')
        trace=[{'payload':{'type':'custom_tool_call','call_id':'read','input':"tools.exec_command({cmd: 'cat contrast.md', workdir: '/trial/plugin'})"}},{'payload':{'type':'custom_tool_call_output','call_id':'read','output':'complete reference'}}]
        self.assertIsNotNone(relative_reference_evidence(trace,p,'complete reference'))
        self.assertIsNone(relative_reference_evidence(trace,Path('/wrong/contrast.md'),'complete reference'))
        self.assertIsNone(relative_reference_evidence(trace,p,'complete reference plus missing tail'))
    def test_unpassed_shell_parameter_is_a_read_failure(self):
        from collect_codex import command_succeeded
        self.assertFalse(command_succeeded({'command':'sed -n 1,260p "$1"','exit_code':1,'aggregated_output':'sed: : No such file or directory'}))
class RelativeRouteControls(unittest.TestCase):
    def test_relative_route_requires_native_cwd_command_and_complete_output(self):
        import tempfile,json
        from collect_codex import permitted_relative_route_read
        with tempfile.TemporaryDirectory() as folder:
            plugin=Path(folder);p=plugin/'skills/design/better-interface/SKILL.md';p.parent.mkdir(parents=True);p.write_text('whole router')
            command={'command':'cat SKILL.md','aggregated_output':'whole router','exit_code':0}
            code='tools.exec_command({cmd: '+json.dumps('cat SKILL.md')+', workdir: '+json.dumps(str(p.parent))+'})'
            trace=[{'payload':{'type':'custom_tool_call','call_id':'r','input':code}},{'payload':{'type':'custom_tool_call_output','call_id':'r','output':'whole router'}}]
            self.assertTrue(permitted_relative_route_read(command,trace,plugin,{'better-interface'}))
            self.assertFalse(permitted_relative_route_read(dict(command,command='cat SKILL.md && git status'),trace,plugin,{'better-interface'}))
            self.assertFalse(permitted_relative_route_read(command,trace,plugin,{'better-colors'}))
            trace[1]['payload']['output']='partial'
            self.assertFalse(permitted_relative_route_read(command,trace,plugin,{'better-interface'}))
class OptionalDiscoveryControls(unittest.TestCase):
    def test_empty_discovery_after_verified_read_is_not_a_read_error(self):
        import tempfile
        from collect_codex import command_succeeded
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'doc.md';p.write_text('whole document')
            command="cat '"+str(p)+"' && pwd && rg --files -g 'AGENTS.md' -g '!node_modules' -g '!vendor' .. && git rev-parse HEAD"
            c={'command':command,'exit_code':1,'aggregated_output':'whole document\n/trial/case\n'}
            self.assertTrue(command_succeeded(c))
            self.assertFalse(command_succeeded(dict(c,aggregated_output='cat: No such file')))
            self.assertFalse(command_succeeded(dict(c,exit_code=2)))
            self.assertFalse(command_succeeded(dict(c,command=command.replace('rg --files','false && rg --files'))))
if __name__=='__main__':unittest.main()
