from pathlib import Path
import json
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/publish-version-tag.mjs'


class ReleaseTagTests(unittest.TestCase):
    def test_publishes_only_version_and_rerun_preserves_tag(self):
        for version in ('0.1.0', '1.0.0'):
            with self.subTest(version=version), tempfile.TemporaryDirectory() as directory:
                self.check_release(Path(directory), version)

    def check_release(self, root, version):
        remote, repo = root / 'remote.git', root / 'repo'
        subprocess.run(['git', 'init', '--bare', '-q', str(remote)], check=True)
        repo.mkdir()
        def git(*args):
            return subprocess.check_output(['git', '-C', str(repo), *args], stderr=subprocess.DEVNULL).decode().strip()
        git('init', '-q', '-b', 'main'); git('config', 'user.name', 'Fixture'); git('config', 'user.email', 'fixture@example.invalid')
        git('remote', 'add', 'origin', str(remote))
        (repo / 'package.json').write_text(json.dumps({'name':'paul-skills','version':version,'private':True}))
        (repo / '.changeset').mkdir()
        (repo / '.changeset/config.json').write_text(json.dumps({'changelog':False,'privatePackages':{'version':True,'tag':True},'baseBranch':'main','access':'restricted'}))
        git('add', '.'); git('commit', '-qm', 'inherited release'); inherited_head = git('rev-parse', 'HEAD')
        for inherited in ('v1.0.0', 'v1.4.0'):
            git('tag', '-a', inherited, '-m', inherited)
            git('push', 'origin', 'refs/tags/' + inherited)
        inherited_refs = git('ls-remote', '--tags', 'origin')
        (repo / 'baseline.md').write_text('Independent Paul version baseline')
        git('add', '.'); git('commit', '-qm', 'release'); head = git('rev-parse', 'HEAD')
        git('tag', 'unrelated-tag')
        subprocess.run(['node', str(SCRIPT)], cwd=repo, check=True, capture_output=True)
        refs = git('ls-remote', '--tags', 'origin')
        tag = 'paul-skills@' + version
        self.assertIn('refs/tags/' + tag, refs)
        self.assertEqual(git('cat-file', '-t', tag), 'tag')
        for line in inherited_refs.splitlines():
            self.assertIn(line, refs)
        self.assertEqual(git('rev-parse', 'v1.0.0^{}'), inherited_head)
        self.assertEqual(len(refs.splitlines()), len(inherited_refs.splitlines()) + 2)
        self.assertNotIn('unrelated-tag', refs)
        (repo / 'note.md').write_text('later docs-only change')
        git('add', '.'); git('commit', '-qm', 'docs')
        subprocess.run(['node', str(SCRIPT)], cwd=repo, check=True, capture_output=True)
        self.assertEqual(git('ls-remote', '--tags', 'origin'), refs)
        self.assertEqual(git('rev-parse', tag + '^{}'), head)

if __name__ == '__main__': unittest.main()
