"""Exercise evidence-version boundaries and corruption rejection locally."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


class EvidenceControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='pm-evidence-control-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for relative in ('evals/product-management-beta', 'evals/pm-conversation-beta',
                         'skills/in-progress/upstream-sync', 'skills/in-progress/office-hours',
                         'skills/in-progress/prototype-user-test', 'skills/in-progress/problem-discovery',
                         'skills/in-progress/product-brief', 'skills/in-progress/experiment-design'):
            shutil.copytree(ROOT / relative, self.root / relative)
        self.history = self.root / 'evals/product-management-beta'
        self.current = self.root / 'evals/pm-conversation-beta'

    def verify(self, folder, *args):
        return subprocess.run([sys.executable, str(folder / 'verify.py'), *args],
                              cwd=self.root, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'),
                              text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def rejected(self, result, message):
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(message, result.stdout)

    def change_skill(self):
        path = self.root / 'skills/in-progress/problem-discovery/SKILL.md'
        path.write_text(path.read_text() + '\nLater local change.\n')

    def test_historical_evidence_survives_current_skill_changes(self):
        self.change_skill()
        result = self.verify(self.history)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn('Current skill equality: not requested', result.stdout)

    def test_current_equality_is_an_explicit_separate_failure(self):
        self.rejected(self.verify(self.history, '--check-current'),
                      'current skill differs from this historical evaluation')

    def test_historical_output_corruption_is_rejected(self):
        trials = json.loads((self.history / 'trials.json').read_text())['trials']
        path = self.history / trials[0]['artifacts'][0]['path']
        path.write_text(path.read_text() + '\nCorrupted output.\n')
        self.rejected(self.verify(self.history), 'artifact drift')

    def test_historical_snapshot_corruption_is_rejected(self):
        trials = json.loads((self.history / 'trials.json').read_text())['trials']
        trial = next(row for row in trials if row['snapshot'])
        path = self.history / trial['snapshot'] / 'SKILL.md'
        path.write_text(path.read_text() + '\nCorrupted snapshot.\n')
        self.rejected(self.verify(self.history), 'snapshot drift')

    def test_historical_origin_revision_corruption_is_rejected(self):
        path = self.history / 'source-baseline.json'
        data = json.loads(path.read_text())
        data['skills'][0]['origins'][0]['importedRevision'] = '0' * 40
        path.write_text(json.dumps(data))
        self.rejected(self.verify(self.history), 'Integrity check failed')

    def test_current_skill_drift_is_rejected_by_later_evidence(self):
        self.change_skill()
        self.rejected(self.verify(self.current), 'Skill tree digest mismatch')

    def test_public_artifact_corruption_is_rejected(self):
        path = self.current / 'RESULTS.md'
        path.write_text(path.read_text() + '\nCorrupted public copy.\n')
        self.rejected(self.verify(self.current), 'Artifact digest mismatch')

    def test_public_copy_ledger_mismatch_is_rejected(self):
        path = self.current / 'public-copy.json'
        data = json.loads(path.read_text())
        data['files'][0]['original_sha256'] = '0' * 64
        path.write_text(json.dumps(data))
        self.rejected(self.verify(self.current), 'Public-copy ledger mismatch')

    def test_unrecorded_public_copy_change_is_rejected(self):
        path = self.current / 'integrity.json'
        data = json.loads(path.read_text())
        data['artifacts']['RESULTS.md'] = '0' * 64
        path.write_text(json.dumps(data))
        self.rejected(self.verify(self.current), 'Unrecorded public-copy change')

    def test_original_manifest_corruption_is_rejected(self):
        path = self.current / 'integrity.original.json'
        path.write_text(path.read_text() + '\n')
        self.rejected(self.verify(self.current), 'Original manifest digest mismatch')


if __name__ == '__main__':
    unittest.main()
