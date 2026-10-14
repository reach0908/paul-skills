"""Missing native loads remain failures even when evidence is internally valid."""
import unittest
from verify_evidence import source_result


class SourceResult(unittest.TestCase):
    case = {'id': 'installed-unknown', 'mode': 'implicit', 'expected': 'better-colors'}

    def test_absent_load_is_false(self):
        row = {'full_body_loads': [], 'checks': {'expected_skill_invoked_and_loaded': False}}
        self.assertFalse(source_result(row, self.case, 'claude', 'correct'))

    def test_absent_load_cannot_claim_pass(self):
        row = {'full_body_loads': [], 'checks': {'expected_skill_invoked_and_loaded': True}}
        with self.assertRaises(AssertionError):
            source_result(row, self.case, 'claude', 'correct')

    def test_wrong_source_cannot_pass(self):
        row = {'loaded_file_hashes': {'better-colors': 'wrong'}, 'checks': {'target_body_equal': True}}
        with self.assertRaises(AssertionError):
            source_result(row, self.case, 'codex', 'correct')

    def test_missing_required_reference_stays_false(self):
        row = {'loaded_file_hashes': {'better-colors': 'correct'},
               'checks': {'target_body_equal': True, 'contrast_reference_fully_read': False},
               'contrast_reference': {'full_body_equal': False}}
        self.assertFalse(source_result(row, dict(self.case, id='installed-resolved'), 'codex', 'correct'))

    def test_full_source_and_reference_pass(self):
        row = {'loaded_file_hashes': {'better-colors': 'correct'},
               'checks': {'target_body_equal': True, 'contrast_reference_fully_read': True},
               'contrast_reference': {'full_body_equal': True}}
        self.assertTrue(source_result(row, dict(self.case, id='installed-resolved'), 'codex', 'correct'))


if __name__ == '__main__':
    unittest.main()
