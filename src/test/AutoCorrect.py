import unittest

from src.AutoCorrect import AutoCorrect


class AutoCorrectTest(unittest.TestCase):
    def test_process_data(self):
        auto_correct = AutoCorrect()
        target = auto_correct.process_data
        test_cases = [ { "name": "default_check", "input": {"file_name": "/../../data/shakespeare.txt"}, "expected": { "expected_output_head": ["o", "for", "a", "muse", "of", "fire", "that", "would", "ascend", "the"], "expected_output_tail": [ "whilst", "you", "abide", "here", "enobarbus", "humbly", "sir", "i", "thank", "you"], "expected_n_words": 6209, }, } ]
        for test_case in test_cases:
            result = target(**test_case["input"])
            self.assertEqual(result[:10], test_case["expected"]["expected_output_head"])
            self.assertEqual(result[-10:], test_case["expected"]["expected_output_tail"])
            self.assertEqual(len(set(result)), test_case["expected"]["expected_n_words"])


if __name__ == '__main__':
    unittest.main()
