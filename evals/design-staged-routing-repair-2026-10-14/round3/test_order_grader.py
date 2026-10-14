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
if __name__=='__main__':unittest.main()
