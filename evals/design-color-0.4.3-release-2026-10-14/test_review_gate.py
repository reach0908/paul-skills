"""Integrity controls, not an automated semantic language judge."""
import json,unittest
from pathlib import Path
from collect import review_matches, current_plugin_loaded
from run_trials import digest,REPO
class ReviewGate(unittest.TestCase):
    def test_retained_failure_remains_red(self):
        d=REPO/'evals/design-routing-0.4.2-release-2026-10-14'
        r=json.loads((d/'codex/normal-better-colors.json').read_text())
        m=json.loads((d/'manual-review.json').read_text())['codex']['normal-better-colors']
        self.assertFalse(r['checks']['semantic_review_pass']);self.assertFalse(review_matches(r['final_response'],m))
    def test_missing_review_fails(self):self.assertFalse(review_matches('response',{}))
    def test_stale_review_fails(self):self.assertFalse(review_matches('new response',{'pass':True,'response_sha256':digest(b'old response'),'reason':'reviewed'}))
    def test_failed_review_fails(self):self.assertFalse(review_matches('response',{'pass':False,'response_sha256':digest(b'response'),'reason':'contradiction'}))
    def test_matching_review_passes(self):self.assertTrue(review_matches('response',{'pass':True,'response_sha256':digest(b'response'),'reason':'consistent with observed evidence'}))
class InstalledVersionGate(unittest.TestCase):
    def test_current_path_and_version(self):self.assertTrue(current_plugin_loaded({'plugins':[{'name':'paul-skills','version':'0.4.3','path':'/expected'}]},'/expected'))
    def test_old_version_fails(self):self.assertFalse(current_plugin_loaded({'plugins':[{'name':'paul-skills','version':'0.4.2','path':'/expected'}]},'/expected'))
    def test_other_path_fails(self):self.assertFalse(current_plugin_loaded({'plugins':[{'name':'paul-skills','version':'0.4.3','path':'/other'}]},'/expected'))
    def test_absent_plugin_fails(self):self.assertFalse(current_plugin_loaded({'plugins':[]},'/expected'))
if __name__=='__main__':unittest.main()
