"""Exercise the shipped wizard library with fake values and no external services."""
import os
from pathlib import Path
import pty
import subprocess
import tempfile
import unittest


TEMPLATE = Path(__file__).resolve().parents[1] / 'skills/engineering/wizard/template.sh'


class WizardTemplateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = TEMPLATE.read_text()
        self.library = self.source.split('# STAGES:')[0]

    def run_bash(self, body, input_text=''):
        return subprocess.run(['/bin/bash', '-c', self.library + '\n' + body],
                              cwd=self.root, input=input_text, text=True,
                              capture_output=True, timeout=5)

    def test_enter_keeps_plain_double_quoted_value_without_quotes(self):
        (self.root / '.env').write_text('EXAMPLE_VALUE="hello world"\n')
        result = self.run_bash('ask EXAMPLE_VALUE "Value:"\n'
                               'write_env EXAMPLE_VALUE "$EXAMPLE_VALUE"', '\n')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.root / '.env').read_text(), "EXAMPLE_VALUE='hello world'\n")

    def test_ambiguous_double_quotes_are_rejected_without_execution(self):
        for value in ['"$OTHER"', '"$(touch injected)"', '"a\\nb"', '"a"b"']:
            with self.subTest(value=value):
                (self.root / '.env').write_text('EXAMPLE_VALUE=' + value + '\n')
                result = self.run_bash('_existing EXAMPLE_VALUE')
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((self.root / 'injected').exists())

    def test_write_is_available_in_later_stage_and_preserves_file_contract(self):
        result = self.run_bash('write_env EXAMPLE_VALUE "first"\n'
                               'write_env EXAMPLE_VALUE "can\'t lose spaces"\n'
                               '[[ "$EXAMPLE_VALUE" == "can\'t lose spaces" ]]\n'
                               '[[ "$(_existing EXAMPLE_VALUE)" == "$EXAMPLE_VALUE" ]]')
        self.assertEqual(result.returncode, 0, result.stderr)
        target = self.root / '.env'
        self.assertEqual(len(target.read_text().splitlines()), 1)
        self.assertEqual(target.stat().st_mode & 0o777, 0o600)

    def test_clear_falls_back_after_tput_failure(self):
        script = self.root / 'clear.sh'
        script.write_text(self.library + '\ntput() { return 1; }\n_clear\nprintf DONE\n')
        master, slave = pty.openpty()
        try:
            process = subprocess.Popen(['/bin/bash', str(script)], stdout=slave, stderr=slave)
            process.wait(timeout=5)
            self.assertEqual(process.returncode, 0, 'terminal clearing exited the script')
            output = os.read(master, 65536)
            self.assertIn(b'\x1b[2J\x1b[3J\x1b[H', output)
            self.assertIn(b'DONE', output)
        finally:
            os.close(slave)
            os.close(master)

    def test_edit_during_prompt_does_not_replace_running_stages(self):
        # Keep the template's stage wrapper and final invocation intact.
        start = self.source.index('TOTAL_STAGES=1')
        end = self.source.index('\nfinish', start)
        stages = 'printf "READY\\n"\nread -r answer\nprintf "FINISHED:%s\\n" "$answer"\n'
        script = self.root / 'wizard.sh'
        script.write_text(self.source[:start] + stages + self.source[end:])
        process = subprocess.Popen(['/bin/bash', str(script)], cwd=self.root,
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=True)
        try:
            self.assertEqual(process.stdout.readline(), 'READY\n')
            script.write_text('this is deliberately invalid bash (\n' * 200)
            output, error = process.communicate('confirmed\n', timeout=5)
            self.assertEqual(process.returncode, 0, error)
            self.assertIn('FINISHED:confirmed', output)
        finally:
            if process.poll() is None:
                process.kill()
                process.communicate()


if __name__ == '__main__':
    unittest.main()
