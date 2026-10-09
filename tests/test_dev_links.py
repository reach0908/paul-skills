from pathlib import Path
import os
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/link-skills.sh'


class DevelopmentLinksTests(unittest.TestCase):
    def test_late_destination_collision_preserves_both_destinations(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            existing = home / '.agents/skills/upstream-sync'
            existing.mkdir(parents=True)
            sentinel = existing / 'my-custom-skill.txt'
            sentinel.write_text('keep this')
            run = subprocess.run(['bash', str(SCRIPT)], env={**os.environ, 'HOME': str(home)}, capture_output=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertEqual(sentinel.read_text(), 'keep this')
            self.assertFalse((home / '.claude').exists())

    def test_fresh_install_is_idempotent_and_links_support_files(self):
        with tempfile.TemporaryDirectory() as directory:
            for _ in range(2):
                subprocess.run(['bash', str(SCRIPT)], env={**os.environ, 'HOME': directory}, check=True, capture_output=True)
            for folder in ['.agents', '.claude']:
                skill = Path(directory) / folder / 'skills/upstream-sync'
                self.assertTrue(skill.is_symlink())
                self.assertTrue((skill / 'scripts/compare.py').is_file())
                self.assertTrue((skill / 'references/provenance.md').is_file())


if __name__ == '__main__': unittest.main()
