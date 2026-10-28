from pathlib import Path
import json
import shutil
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/sync-plugin-version.mjs'
SKILLS = ['./skills/engineering/tdd', './skills/design/better-ui']


class PluginVersionSyncTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        (self.root / 'scripts').mkdir()
        shutil.copy(SCRIPT, self.root / 'scripts')
        claude = {
            'name': 'paul-skills', 'version': '0.5.0', 'description': 'Skills.',
            'author': {'name': 'Paul Kim', 'url': 'https://github.com/reach0908'},
            'homepage': 'https://github.com/reach0908/paul-skills',
            'repository': 'https://github.com/reach0908/paul-skills',
            'license': 'MIT', 'keywords': ['skills'], 'skills': SKILLS,
        }
        cursor = {key: value for key, value in claude.items() if key != 'author'}
        cursor.update(displayName='Paul Skills', author={'name': 'Paul Kim'})
        self.write('package.json', {'name': 'paul-skills', 'version': '0.6.0'})
        self.write('.claude-plugin/plugin.json', claude)
        self.write('.cursor-plugin/plugin.json', cursor)
        self.write('package-lock.json', {'name': 'paul-skills', 'version': '0.5.0', 'packages': {'': {'version': '0.5.0'}}})

    def write(self, name, value):
        path = self.root / name
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps(value, indent=2) + '\n')

    def read(self, name):
        return json.loads((self.root / name).read_text())

    def run_script(self, *args):
        return subprocess.run(['node', 'scripts/sync-plugin-version.mjs', *args], cwd=self.root, capture_output=True, text=True)

    def test_sync_writes_both_manifests_and_lock(self):
        self.assertEqual(self.run_script().returncode, 0)
        claude, cursor = self.read('.claude-plugin/plugin.json'), self.read('.cursor-plugin/plugin.json')
        self.assertEqual(claude['version'], '0.6.0')
        self.assertEqual(cursor['version'], '0.6.0')
        self.assertEqual(self.read('package-lock.json')['packages']['']['version'], '0.6.0')
        self.assertEqual(cursor['skills'], SKILLS)
        self.assertEqual(cursor['author'], {'name': 'Paul Kim'})
        self.assertEqual(cursor['displayName'], 'Paul Skills')
        self.assertEqual(self.run_script('--check').returncode, 0)

    def test_sync_copies_shared_fields_from_claude_manifest(self):
        cursor = self.read('.cursor-plugin/plugin.json')
        cursor.update(skills=SKILLS[:1], author={'name': 'Someone Else', 'email': 'a@example.invalid'})
        self.write('.cursor-plugin/plugin.json', cursor)
        self.assertEqual(self.run_script().returncode, 0)
        cursor = self.read('.cursor-plugin/plugin.json')
        self.assertEqual(cursor['skills'], SKILLS)
        self.assertEqual(cursor['author'], {'name': 'Paul Kim', 'email': 'a@example.invalid'})

    def test_check_reports_version_and_shared_field_drift_without_writing(self):
        self.assertEqual(self.run_script().returncode, 0)
        drifts = {
            'version': '0.5.0', 'name': 'other', 'description': 'Other.', 'license': 'Apache-2.0',
            'homepage': 'https://example.invalid', 'repository': 'https://example.invalid',
            'keywords': [], 'skills': SKILLS[:1], 'author': {'name': 'Someone Else'},
        }
        baseline = self.read('.cursor-plugin/plugin.json')
        for field, value in drifts.items():
            with self.subTest(field=field):
                self.write('.cursor-plugin/plugin.json', {**baseline, field: value})
                before = (self.root / '.cursor-plugin/plugin.json').read_text()
                result = self.run_script('--check')
                self.assertEqual(result.returncode, 1)
                self.assertIn('.cursor-plugin/plugin.json ' + ('author.name' if field == 'author' else field), result.stderr)
                self.assertEqual((self.root / '.cursor-plugin/plugin.json').read_text(), before)

    def test_check_reports_claude_manifest_version_drift(self):
        self.assertEqual(self.run_script().returncode, 0)
        self.write('package.json', {'name': 'paul-skills', 'version': '0.7.0'})
        result = self.run_script('--check')
        self.assertEqual(result.returncode, 1)
        self.assertIn('.claude-plugin/plugin.json version', result.stderr)


if __name__ == '__main__': unittest.main()
