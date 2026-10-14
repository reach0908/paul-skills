"""Positive and negative controls for narrowly replayed Git query outcomes."""
from pathlib import Path
import subprocess,tempfile,unittest
from expected_git_results import confirm_git_query_result
class GitResultControls(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
  self.git('init','-q','-b','main');(self.root/'src').mkdir();(self.root/'src/Panel.html').write_text('panel\n')
  self.git('add','src/Panel.html');self.git('-c','user.name=Fixture','-c','user.email=fixture@example.invalid','-c','commit.gpgsign=false','commit','-qm','base')
  (self.root/'src/New.html').write_text('new action\n')
 def tearDown(self):self.tmp.cleanup()
 def git(self,*args):return subprocess.run(['git','-c','core.hooksPath=/dev/null',*args],cwd=self.root,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 def probe(self,cmd,code,output):return confirm_git_query_result({'command':cmd,'exit_code':code,'aggregated_output':output},str(self.root))
 def absence(self):return self.probe('git cat-file -e HEAD:src/New.html',128,"fatal: path 'src/New.html' exists on disk, but not in 'HEAD'\n")
 def test_valid_untracked_absence(self):self.assertIsNotNone(self.absence())
 def test_tracked_file_is_not_absence(self):
  self.git('add','src/New.html');self.assertIsNone(self.absence())
 def test_missing_disk_file_is_not_absence(self):
  (self.root/'src/New.html').unlink();self.assertIsNone(self.absence())
 def test_output_must_match(self):self.assertIsNone(self.probe('git cat-file -e HEAD:src/New.html',128,'permission denied'))
 def test_plain_content_read_is_not_probe(self):self.assertIsNone(self.probe('git show HEAD:src/New.html',128,"fatal: path 'src/New.html' exists on disk, but not in 'HEAD'\n"))
 def test_valid_no_match(self):self.assertIsNotNone(self.probe('git grep -n -e New.html -e new-action HEAD -- .',1,''))
 def test_chained_command_is_rejected(self):self.assertIsNone(self.probe('git grep -n -e New.html -e new-action HEAD -- . && cat missing',1,''))
 def test_invalid_head_is_not_no_match(self):self.assertIsNone(self.probe('git grep -n -e New.html -e new-action BAD_HEAD -- .',1,''))
if __name__=='__main__':unittest.main()
