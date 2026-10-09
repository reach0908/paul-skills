import copy
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[1] / 'skills/engineering/upstream-sync/scripts/compare.py'
spec = importlib.util.spec_from_file_location('compare', MODULE)
compare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compare)


class CompareTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / 'source'
        self.local = self.root / 'local'
        self.source.mkdir()
        self.local.mkdir()
        self.g('init', '-q')
        self.g('config', 'user.name', 'Fixture')
        self.g('config', 'user.email', 'fixture@example.invalid')
        self.put(self.source, 'skills/demo/SKILL.md', 'Base instructions\n')
        self.put(self.source, 'skills/demo/references/rules.md', 'Base support\n')
        self.base = self.commit('base')
        self.put(self.local, 'skills/demo/SKILL.md', 'Base instructions\n')
        self.put(self.local, 'skills/demo/references/rules.md', 'Base support\n')
        self.registry = {'schemaVersion': 1, 'sources': {'source': {'repository': 'https://example.invalid/source', 'repositoryReview': self.base}}, 'skills': [{'id': 'demo', 'path': 'skills/demo', 'origins': [{'source': 'source', 'path': 'skills/demo', 'importedRevision': self.base, 'reviewedRevision': self.base, 'localDigest': compare.digest(compare.local_tree(self.local, 'skills/demo')), 'decisions': []}]}]}

    def g(self, *args):
        return subprocess.check_output(['git', '-C', str(self.source), *args], stderr=subprocess.DEVNULL).decode().strip()

    def put(self, root, path, text):
        p = root / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)

    def commit(self, message):
        self.g('add', '.')
        self.g('commit', '-qm', message)
        return self.g('rev-parse', 'HEAD')

    def run_report(self, target=None):
        return compare.report(self.registry, 'source', self.source, target or self.base, self.local)

    def test_unchanged_is_read_only(self):
        before = copy.deepcopy(self.registry)
        result = self.run_report()
        self.assertEqual(result['skills'][0]['status'], 'UNCHANGED')
        self.assertEqual(self.registry, before)
        self.assertEqual(self.g('status', '--porcelain'), '')

    def test_three_way_preserves_local_and_catches_support_changes(self):
        self.put(self.local, 'skills/demo/SKILL.md', 'Local Korean policy\n')
        self.put(self.source, 'skills/demo/references/rules.md', 'New upstream support\n')
        target = self.commit('support change')
        row = self.run_report(target)['skills'][0]
        self.assertEqual(row['upstreamChanges'], [{'path': 'references/rules.md', 'change': 'modified'}])
        self.assertEqual(row['localChanges'], [{'path': 'SKILL.md', 'change': 'modified'}])
        self.assertTrue(row['localDrift'])
        self.assertEqual((self.local / 'skills/demo/SKILL.md').read_text(), 'Local Korean policy\n')

    def test_same_head_does_not_hide_local_edit(self):
        self.put(self.local, 'skills/demo/SKILL.md', 'New local work')
        self.assertEqual(self.run_report()['skills'][0]['status'], 'REVIEW')

    def test_deferred_work_does_not_disappear(self):
        self.registry['skills'][0]['origins'][0]['decisions'] = [{'decision': 'defer', 'reason': 'dependency unavailable'}]
        self.assertEqual(self.run_report()['skills'][0]['status'], 'REVIEW')

    def test_missing_source_path_is_unknown_and_rename_is_visible(self):
        (self.source / 'skills/demo').rename(self.source / 'skills/renamed')
        data = self.run_report(self.commit('rename'))
        self.assertEqual(data['status'], 'UNKNOWN')
        self.assertIn('skills/renamed', data['newCandidates'])
        self.assertIn('R100', data['repositoryChanges'])

    def test_unknown_history_is_not_unchanged(self):
        self.registry['skills'][0]['origins'][0]['reviewedRevision'] = '0' * 40
        self.assertEqual(self.run_report()['skills'][0]['status'], 'UNKNOWN')

    def test_path_escape_is_rejected(self):
        self.registry['skills'][0]['path'] = '../source/skills/demo'
        self.assertEqual(self.run_report()['skills'][0]['status'], 'UNKNOWN')

    def test_symlink_is_rejected_without_reading_target(self):
        (self.local / 'skills/demo/secret').symlink_to(self.root / 'outside')
        self.assertEqual(self.run_report()['skills'][0]['status'], 'UNKNOWN')

    def test_execution_mode_change_is_detected(self):
        (self.local / 'skills/demo/SKILL.md').chmod(0o755)
        self.assertTrue(self.run_report()['skills'][0]['localDrift'])

    def test_multiple_sources_are_independent(self):
        self.registry['sources']['other'] = copy.deepcopy(self.registry['sources']['source'])
        second = copy.deepcopy(self.registry['skills'][0]['origins'][0])
        second.update(source='other', reviewedRevision='0' * 40)
        self.registry['skills'][0]['origins'].append(second)
        self.assertEqual(self.run_report()['skills'][0]['status'], 'UNCHANGED')
        result = compare.report(self.registry, 'other', self.source, self.base, self.local)
        self.assertEqual(result['status'], 'UNKNOWN')

    def test_missing_repository_review_is_explicit(self):
        del self.registry['sources']['source']['repositoryReview']
        self.assertEqual(self.run_report()['status'], 'UNKNOWN')

    def test_ref_names_are_not_accepted_as_pins(self):
        with self.assertRaises(ValueError):
            self.run_report('HEAD')


if __name__ == '__main__':
    unittest.main()
