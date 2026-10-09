#!/usr/bin/env python3
"""Pass a saved research brief to Aside without interpreting it as shell code."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true', help='Check availability only')
    mode.add_argument('--prompt-file', type=Path, help='Absolute path to a UTF-8 brief')
    parser.add_argument('--effort', default='ultrabrowse',
                        choices=['default', 'off', 'minimal', 'low', 'medium', 'high',
                                 'xhigh', 'max', 'ultrabrowse'])
    followup = parser.add_mutually_exclusive_group()
    followup.add_argument('--resume', help='Resume a known Aside session')
    followup.add_argument('--steer', help='Redirect a known running Aside session')
    followup.add_argument('--queue', help='Queue a follow-up for a known Aside session')
    args = parser.parse_args(argv)
    action = next((name for name in ['resume', 'steer', 'queue'] if getattr(args, name)), None)
    session = getattr(args, action) if action else None
    if session and (args.check or args.effort != 'ultrabrowse'):
        parser.error('Session follow-ups require a prompt and retain the session effort')
    if session and session.startswith('-'):
        parser.error('A session ID cannot start with a dash')
    prompt = None
    if args.prompt_file:
        if not args.prompt_file.is_absolute():
            parser.error('--prompt-file must be an absolute path')
        try:
            prompt = args.prompt_file.read_text(encoding='utf-8')
        except (OSError, UnicodeError) as exc:
            parser.error(f'Cannot read brief: {exc}')
        if not prompt.strip() or '\0' in prompt:
            parser.error('The brief must be nonempty UTF-8 text without NUL bytes')
    executable = shutil.which('aside')
    if not executable:
        print('Aside CLI unavailable (PATH lookup failed). Preserve the brief; '
              'ask the user to restore Aside or authorize another web engine.', file=sys.stderr)
        return 2
    try:
        version = subprocess.run([executable, '--version'], capture_output=True,
                                 text=True, timeout=15, check=True)
        print(f'Aside: {executable} ({version.stdout.strip()})', file=sys.stderr)
        if args.check:
            return 0
        if session:
            command = [executable, 'session', action, session]
        else:
            command = [executable, 'exec']
            if args.effort != 'default':
                command.extend(['--effort', args.effort])
        command.extend(['--', prompt])
        return subprocess.run(command).returncode
    except subprocess.CalledProcessError as exc:
        print(f'Aside version check failed (exit {exc.returncode}): '
              f'{(exc.stderr or "").strip()}', file=sys.stderr)
        return exc.returncode
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f'Aside failed: {exc}. Preserve the brief and any partial output.', file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print('Aside observation interrupted; retain partial output and the session ID.',
              file=sys.stderr)
        return 130


if __name__ == '__main__':
    sys.exit(main())
