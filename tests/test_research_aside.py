import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


HELPER = Path(__file__).resolve().parents[1] / 'skills/engineering/research/scripts/aside_research.py'


class AsideResearchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.log = self.root / 'arguments.jsonl'
        self.brief = self.root / 'brief with spaces.txt'
        self.brief.write_text('Read an original source and return evidence.\n')
        self.binary = self.root / 'aside'
        self.binary.write_text(f'#!{sys.executable}\n' + '''import json, os, sys
from pathlib import Path
with Path(os.environ['ASIDE_TEST_LOG']).open('a') as log:
    log.write(json.dumps(sys.argv[1:]) + '\\n')
if sys.argv[1:] == ['--version']:
    print('fixture-version')
    sys.exit(int(os.environ.get('ASIDE_TEST_VERSION_EXIT', '0')))
print('Fixture report with original evidence')
sys.exit(int(os.environ.get('ASIDE_TEST_RUN_EXIT', '0')))
''')
        self.binary.chmod(0o755)
        self.env = {**os.environ, 'PATH': str(self.root), 'ASIDE_TEST_LOG': str(self.log)}

    def run_helper(self, *args, env=None):
        return subprocess.run([sys.executable, str(HELPER), *args],
                              env=env or self.env, text=True, capture_output=True, timeout=10)

    def calls(self):
        return [json.loads(line) for line in self.log.read_text().splitlines()] if self.log.exists() else []

    def test_check_does_not_start_research(self):
        result = self.run_helper('--check')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.calls(), [['--version']])

    def test_prompt_is_one_literal_argument_and_report_streams(self):
        marker = self.root / 'shell-executed'
        text = f'--account u9\n한국어 "quotes" $(touch {marker}) `touch {marker}`\n'
        self.brief.write_text(text)
        result = self.run_helper('--prompt-file', str(self.brief))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.calls(), [['--version'], ['exec', '--effort', 'ultrabrowse', '--', text]])
        self.assertIn('Fixture report', result.stdout)
        self.assertFalse(marker.exists())

    def test_missing_cli_preserves_brief_and_reports_failure(self):
        self.binary.unlink()
        before = self.brief.read_bytes()
        result = self.run_helper('--prompt-file', str(self.brief))
        self.assertEqual(result.returncode, 2)
        self.assertIn('Aside CLI unavailable', result.stderr)
        self.assertEqual(self.brief.read_bytes(), before)
        self.assertEqual(self.calls(), [])

    def test_failed_version_check_stops_before_discovery(self):
        result = self.run_helper('--prompt-file', str(self.brief),
                                 env={**self.env, 'ASIDE_TEST_VERSION_EXIT': '7'})
        self.assertEqual(result.returncode, 7)
        self.assertEqual(self.calls(), [['--version']])

    def test_execution_failure_is_visible(self):
        result = self.run_helper('--prompt-file', str(self.brief),
                                 env={**self.env, 'ASIDE_TEST_RUN_EXIT': '9'})
        self.assertEqual(result.returncode, 9)
        self.assertIn('Fixture report', result.stdout)

    def test_default_effort_preserves_user_configuration(self):
        result = self.run_helper('--prompt-file', str(self.brief), '--effort', 'default')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.calls()[1], ['exec', '--', self.brief.read_text()])

    def test_resume_uses_known_session_without_overriding_settings(self):
        result = self.run_helper('--prompt-file', str(self.brief), '--resume', 'ses_known')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.calls()[1], ['session', 'resume', 'ses_known', '--', self.brief.read_text()])

    def test_running_followup_preserves_literal_prompt(self):
        self.brief.write_text('Correct "scope" and keep $HOME literal.\n')
        for action in ['steer', 'queue']:
            with self.subTest(action=action):
                self.log.unlink(missing_ok=True)
                result = self.run_helper('--prompt-file', str(self.brief), '--' + action, 'ses_owned')
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(self.calls()[1], ['session', action, 'ses_owned', '--', self.brief.read_text()])

    def test_invalid_session_never_starts_a_new_investigation(self):
        for action in ['resume', 'steer', 'queue']:
            for session in ['', '   ', ' ses_known', 'ses_known ', '-invalid']:
                with self.subTest(action=action, session=session):
                    self.log.unlink(missing_ok=True)
                    result = self.run_helper('--prompt-file', str(self.brief),
                                             '--' + action + '=' + session)
                    self.assertEqual(result.returncode, 2, result.stdout)
                    self.assertEqual(self.calls(), [])

    def test_followup_rejects_check_and_explicit_effort(self):
        for options in [('--check',), ('--prompt-file', str(self.brief), '--effort', 'default'),
                        ('--prompt-file', str(self.brief), '--effort', 'ultrabrowse')]:
            with self.subTest(options=options):
                self.log.unlink(missing_ok=True)
                result = self.run_helper(*options, '--resume', 'ses_known')
                self.assertEqual(result.returncode, 2, result.stdout)
                self.assertEqual(self.calls(), [])

    def test_invalid_brief_never_launches_aside(self):
        for text in ['', '   ', 'invalid\0brief']:
            with self.subTest(text=text):
                self.brief.write_text(text)
                result = self.run_helper('--prompt-file', str(self.brief))
                self.assertEqual(result.returncode, 2)
                self.assertEqual(self.calls(), [])


if __name__ == '__main__':
    unittest.main()
