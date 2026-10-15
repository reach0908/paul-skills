"""Guard evidence boundaries, including honestly retained failed trials."""
from pathlib import Path
import tempfile,unittest
from verify import sha,checked_response,check_review
from collect import full_read,numbered_lines

class EvidenceTests(unittest.TestCase):
 def test_changed_response_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);(root/'answer.md').write_text('observed answer')
   receipt={'response':'answer.md','response_sha256':sha(b'observed answer')}
   checked_response(receipt,root);(root/'answer.md').write_text('edited answer')
   with self.assertRaises(AssertionError):checked_response(receipt,root)
 def test_stale_semantic_judgment_rejected(self):
  with self.assertRaises(AssertionError):check_review({'completed':True,'response_sha256':'a'},{'status':'reviewed','response_sha256':'b','criteria':{},'evidence':[]})
 def test_incomplete_is_retained_but_not_scored(self):
  receipt={'completed':False,'response_sha256':'a'}
  check_review(receipt,{'status':'not_assessed','response_sha256':'a'})
  with self.assertRaises(AssertionError):check_review(receipt,{'status':'reviewed','response_sha256':'a','criteria':{'safe':True},'evidence':['partial answer']})
 def test_full_reference_requires_all_original_lines(self):
  expected='first\n\nlast\n'
  self.assertTrue(full_read(expected,numbered_lines('1\tfirst\n2\t\n3\tlast')))
  self.assertFalse(full_read(expected,numbered_lines('1\tfirst\n3\tlast')))
  self.assertFalse(full_read(expected,numbered_lines('1\tfirst\n2\t\n3\tchanged')))

if __name__=='__main__':unittest.main()
