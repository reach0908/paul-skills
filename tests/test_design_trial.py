import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch


MODULE = Path(__file__).resolve().parents[1] / 'evals/design-beta/prepare_trial.py'
spec = importlib.util.spec_from_file_location('design_trial', MODULE)
trial = importlib.util.module_from_spec(spec)
spec.loader.exec_module(trial)


class DesignTrialTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.here = self.root / 'eval'
        (self.here / 'cases').mkdir(parents=True)
        (self.here / 'cases/inflfeed.md').write_text('Review the whole page.\n')
        self.upstream = self.root / 'upstream'
        self.upstream.mkdir()
        self.git('init', '-q')
        (self.upstream / 'skills/review').mkdir(parents=True)
        files = {'skills/review/SKILL.md': b'original\n', 'LICENSE': b'notice\n'}
        for path, data in files.items():
            (self.upstream / path).write_bytes(data)
        self.git('add', '.')
        self.git('-c', 'user.name=Trial', '-c', 'user.email=trial@example.invalid',
                 '-c', 'core.hooksPath=/dev/null', 'commit', '-qm', 'fixture')
        revision = self.git('rev-parse', 'HEAD').strip()
        manifest = {'revision': revision, 'files': {
            p: hashlib.sha256(data).hexdigest() for p, data in files.items()}}
        (self.here / 'upstream-manifest.json').write_text(json.dumps(manifest))
        for name in ['review', 'design-browser']:
            folder = self.root / 'skills/in-progress' / name
            folder.mkdir(parents=True)
            (folder / 'SKILL.md').write_text('candidate ' + name)
        (self.root / 'skill-sources.json').write_text(json.dumps({'skills': [
            {'id': name, 'path': 'skills/in-progress/' + name}
            for name in ['review', 'design-browser']]}))
        self.addCleanup(patch.stopall)
        patch.object(trial, 'HERE', self.here).start()
        patch.object(trial, 'ROOT', self.root).start()

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.upstream), *args], text=True)

    def test_arms_share_task_but_not_skills(self):
        records = [trial.prepare(self.root / ('trial-' + arm), arm, self.upstream)
                   for arm in ['no-skill', 'upstream', 'paul']]
        self.assertEqual(len({r['taskDigest'] for r in records}), 1)
        self.assertEqual(records[0]['skillFiles'], {})
        self.assertNotEqual(records[1]['bundleDigest'], records[2]['bundleDigest'])
        self.assertEqual((self.root / 'upstream' / 'skills/review/SKILL.md').read_text(), 'original\n')

    def test_source_uses_commit_not_dirty_checkout(self):
        (self.upstream / 'skills/review/SKILL.md').write_text('dirty')
        trial.prepare(self.root / 'out', 'upstream', self.upstream)
        self.assertEqual((self.root / 'out/.agents/skills/review/SKILL.md').read_text(), 'original\n')
        self.assertEqual((self.root / 'out/.agents/skills/review/LICENSE').read_text(), 'notice\n')

    def test_existing_destination_preserved(self):
        with self.assertRaises(ValueError):
            trial.prepare(self.here, 'no-skill')
        self.assertTrue((self.here / 'cases/inflfeed.md').is_file())

    def test_hash_mismatch_leaves_no_output(self):
        p = self.here / 'upstream-manifest.json'
        manifest = json.loads(p.read_text())
        manifest['files']['LICENSE'] = '0' * 64
        p.write_text(json.dumps(manifest))
        with self.assertRaises(ValueError):
            trial.prepare(self.root / 'out', 'upstream', self.upstream)
        self.assertFalse((self.root / 'out').exists())

    def test_missing_candidate_leaves_no_output(self):
        (self.root / 'skills/in-progress/review/SKILL.md').unlink()
        with self.assertRaises(ValueError):
            trial.prepare(self.root / 'out', 'paul')
        self.assertFalse((self.root / 'out').exists())

    def test_promoted_candidate_uses_registered_location(self):
        (self.root / 'skills/design').mkdir()
        shutil.move(self.root / 'skills/in-progress/review', self.root / 'skills/design/review')
        p = self.root / 'skill-sources.json'
        registry = json.loads(p.read_text())
        registry['skills'][0]['path'] = 'skills/design/review'
        p.write_text(json.dumps(registry))
        trial.prepare(self.root / 'out', 'paul')
        self.assertEqual((self.root / 'out/.agents/skills/review/SKILL.md').read_text(), 'candidate review')

    def test_ambiguous_inventory_leaves_no_output(self):
        p = self.root / 'skill-sources.json'
        registry = json.loads(p.read_text())
        registry['skills'].append(registry['skills'][0])
        p.write_text(json.dumps(registry))
        with self.assertRaises(ValueError):
            trial.prepare(self.root / 'out', 'paul')
        self.assertFalse((self.root / 'out').exists())


if __name__ == '__main__':
    unittest.main()
