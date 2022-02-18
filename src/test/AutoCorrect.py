import collections
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

    def test_get_count(self):
        auto_correct = AutoCorrect()
        target = auto_correct.get_count
        word_l = auto_correct.process_data("/../../data/shakespeare.txt")
        test_cases = [
            {
                "name": "default_check",
                "input": {"word_l": word_l},
                "expected": {
                    "expected_key_value_pairs": 6209,
                    "expected_count_thee": 240,
                    "expected_count_esteemed": 3,
                    "expected_count_your": 397,
                },
            },
            {
                "name": "small_head_set_check",
                "input": {"word_l": word_l[:1000]},
                "expected": {
                    "expected_key_value_pairs": 494,
                    "expected_count_thee": 0,
                    "expected_count_esteemed": -1,
                    "expected_count_your": 4,
                },
            },
            {
                "name": "medium_tail_set_check",
                "input": {"word_l": word_l[-10000:]},
                "expected": {
                    "expected_key_value_pairs": 2184,
                    "expected_count_thee": 18,
                    "expected_count_esteemed": 1,
                    "expected_count_your": 61,
                },
            },
        ]
        for test_case in test_cases:
            result = target(**test_case["input"])
            self.assertEqual(True, isinstance(result, collections.Counter) or isinstance(result, dict))
            self.assertEqual(len(result), test_case["expected"]["expected_key_value_pairs"])
            self.assertEqual(True, result.get("thee", 0) == test_case["expected"]["expected_count_thee"])
            self.assertEqual (True, result.get("esteemed", -1) == test_case["expected"]["expected_count_esteemed"])
            self.assertEqual(result.get("your", 0), test_case["expected"]["expected_count_your"])

    def test_get_probs(self):
        auto_correct = AutoCorrect()
        target = auto_correct.get_probs
        word_l = auto_correct.process_data("/../../data/shakespeare.txt")
        word_count_dict = auto_correct.get_count(word_l)
        test_cases = [
            {
                "name": "default_check",
                "input": {"word_count_dict": word_count_dict},
                "expected": {
                    "expected_prob_length": 6209,
                    "expected_prob_thee": 0.0045,
                    "expected_prob_esteemed": 0.0001,
                    "expected_prob_your": 0.0074,
                },
            },
            {
                "name": "small_check",
                "input": {
                    "word_count_dict": {
                        key: word_count_dict[key]
                        for key in [
                            "for",
                            "a",
                            "fire",
                            "ascend",
                            "esteemed",
                            "your",
                            "thee",
                        ]
                    }
                },
                "expected": {
                    "expected_prob_length": 7,
                    "expected_prob_thee": 0.1267,
                    "expected_prob_esteemed": 0.0016,
                    "expected_prob_your": 0.2096,
                },
            },
        ]
        for test_case in test_cases:
            result = target(**test_case["input"])
            self.assertEqual(True, isinstance(result, dict))
            self.assertEqual(len(result), test_case["expected"]["expected_prob_length"])
            self.assertEqual(True, abs(round(result["thee"], 4) - round(test_case["expected"]["expected_prob_thee"], 4)) < .1)
            self.assertEqual(True, abs(round(result["esteemed"], 4) - round(test_case["expected"]["expected_prob_esteemed"], 4)) < .1)
            self.assertEqual(True, abs(round(result["your"], 4) - round(test_case["expected"]["expected_prob_your"], 4)) < .1)

    def test_delete_letter(self):
        auto_correct = AutoCorrect()
        target = auto_correct.delete_letter
        test_cases = [
            {
                "name": "default_check",
                "input": {"word": "cans"},
                "expected": ["ans", "cns", "cas", "can"],
            },
            {
                "name": "small_default_check",
                "input": {"word": "at"},
                "expected": ["t", "a"],
            },
            {
                "name": "long_check",
                "input": {"word": "esteemed"},
                "expected": [
                    "steemed",
                    "eteemed",
                    "eseemed",
                    "estemed",
                    "estemed",
                    "esteeed",
                    "esteemd",
                    "esteeme",
                ],
            },
        ]
        for test_case in test_cases:
            result = target(**test_case["input"])
            self.assertEqual(True, isinstance(result, list))
            self.assertEqual(sorted(result), sorted(test_case["expected"]))

    def test_switch_letter(self):
        auto_correct = AutoCorrect()
        target = auto_correct.switch_letter
        test_cases = [
            {
                "name": "default_check",
                "input": {"word": "eta"},
                "expected": ["tea", "eat"],
            },
            {"name": "small_default_check", "input": {"word": "at"}, "expected": ["ta"], },
            {
                "name": "long_check",
                "input": {"word": "satr"},
                "expected": ["astr", "star", "sart"],
            },
        ]
        for test_case in test_cases:
            result = target(**test_case["input"])
            self.assertEqual(True, isinstance(result, list))

    def test_replace_letter(self):
        auto_correct = AutoCorrect()
        target = auto_correct.replace_letter
        test_cases = [
            {
                "name": "default_check",
                "input": {"word": "can"},
                "expected": ['aan', 'ban', 'caa', 'cab', 'cac', 'cad', 'cae', 'caf', 'cag', 'cah', 'cai', 'caj', 'cak', 'cal', 'cam', 'cao', 'cap', 'caq', 'car', 'cas', 'cat', 'cau', 'cav', 'caw', 'cax', 'cay', 'caz', 'cbn', 'ccn', 'cdn', 'cen', 'cfn', 'cgn', 'chn', 'cin', 'cjn', 'ckn', 'cln', 'cmn', 'cnn', 'con', 'cpn', 'cqn', 'crn', 'csn', 'ctn', 'cun', 'cvn', 'cwn', 'cxn', 'cyn', 'czn', 'dan', 'ean', 'fan', 'gan', 'han', 'ian', 'jan', 'kan', 'lan', 'man', 'nan', 'oan', 'pan', 'qan', 'ran', 'san', 'tan', 'uan', 'van', 'wan', 'xan', 'yan', 'zan'],
            },
            {
                "name": "small_default_check",
                "input": {"word": "at"},
                "expected": [
                    "aa",
                    "ab",
                    "ac",
                    "ad",
                    "ae",
                    "af",
                    "ag",
                    "ah",
                    "ai",
                    "aj",
                    "ak",
                    "al",
                    "am",
                    "an",
                    "ao",
                    "ap",
                    "aq",
                    "ar",
                    "as",
                    "au",
                    "av",
                    "aw",
                    "ax",
                    "ay",
                    "az",
                    "bt",
                    "ct",
                    "dt",
                    "et",
                    "ft",
                    "gt",
                    "ht",
                    "it",
                    "jt",
                    "kt",
                    "lt",
                    "mt",
                    "nt",
                    "ot",
                    "pt",
                    "qt",
                    "rt",
                    "st",
                    "tt",
                    "ut",
                    "vt",
                    "wt",
                    "xt",
                    "yt",
                    "zt",
                ],
            },
            {
                "name": "long_check",
                "input": {"word": "star"},
                "expected": [
                    "atar",
                    "btar",
                    "ctar",
                    "dtar",
                    "etar",
                    "ftar",
                    "gtar",
                    "htar",
                    "itar",
                    "jtar",
                    "ktar",
                    "ltar",
                    "mtar",
                    "ntar",
                    "otar",
                    "ptar",
                    "qtar",
                    "rtar",
                    "saar",
                    "sbar",
                    "scar",
                    "sdar",
                    "sear",
                    "sfar",
                    "sgar",
                    "shar",
                    "siar",
                    "sjar",
                    "skar",
                    "slar",
                    "smar",
                    "snar",
                    "soar",
                    "spar",
                    "sqar",
                    "srar",
                    "ssar",
                    "staa",
                    "stab",
                    "stac",
                    "stad",
                    "stae",
                    "staf",
                    "stag",
                    "stah",
                    "stai",
                    "staj",
                    "stak",
                    "stal",
                    "stam",
                    "stan",
                    "stao",
                    "stap",
                    "staq",
                    "stas",
                    "stat",
                    "stau",
                    "stav",
                    "staw",
                    "stax",
                    "stay",
                    "staz",
                    "stbr",
                    "stcr",
                    "stdr",
                    "ster",
                    "stfr",
                    "stgr",
                    "sthr",
                    "stir",
                    "stjr",
                    "stkr",
                    "stlr",
                    "stmr",
                    "stnr",
                    "stor",
                    "stpr",
                    "stqr",
                    "strr",
                    "stsr",
                    "sttr",
                    "stur",
                    "stvr",
                    "stwr",
                    "stxr",
                    "styr",
                    "stzr",
                    "suar",
                    "svar",
                    "swar",
                    "sxar",
                    "syar",
                    "szar",
                    "ttar",
                    "utar",
                    "vtar",
                    "wtar",
                    "xtar",
                    "ytar",
                    "ztar",
                ],
            },
        ]
        for test_case in test_cases:
            result = target(**test_case["input"])
            self.assertEqual(True, isinstance(result, list))
            self.assertEqual(len(set(map(len, result))),  1)
            self.assertEqual(sorted(result), sorted(test_case["expected"]))

    def test_insert_letter(self):
        auto_correct = AutoCorrect()
        target = auto_correct.insert_letter
        test_cases = [
            {
                "name": "default_check",
                "input": {"word": "at"},
                "expected": ['aat', 'bat', 'cat', 'dat', 'eat', 'fat', 'gat', 'hat', 'iat', 'jat', 'kat', 'lat', 'mat', 'nat', 'oat', 'pat', 'qat', 'rat', 'sat', 'tat', 'uat', 'vat', 'wat', 'xat', 'yat', 'zat', 'aat', 'abt', 'act', 'adt', 'aet', 'aft', 'agt', 'aht', 'ait', 'ajt', 'akt', 'alt', 'amt', 'ant', 'aot', 'apt', 'aqt', 'art', 'ast', 'att', 'aut', 'avt', 'awt', 'axt', 'ayt', 'azt'],
            },
            {
                "name": "long_check",
                "input": {"word": "can"},
                "expected": ['acan', 'bcan', 'ccan', 'dcan', 'ecan', 'fcan', 'gcan', 'hcan', 'ican', 'jcan', 'kcan', 'lcan', 'mcan', 'ncan', 'ocan', 'pcan', 'qcan', 'rcan', 'scan', 'tcan', 'ucan', 'vcan', 'wcan', 'xcan', 'ycan', 'zcan', 'caan', 'cban', 'ccan', 'cdan', 'cean', 'cfan', 'cgan', 'chan', 'cian', 'cjan', 'ckan', 'clan', 'cman', 'cnan', 'coan', 'cpan', 'cqan', 'cran', 'csan', 'ctan', 'cuan', 'cvan', 'cwan', 'cxan', 'cyan', 'czan', 'caan', 'cabn', 'cacn', 'cadn', 'caen', 'cafn', 'cagn', 'cahn', 'cain', 'cajn', 'cakn', 'caln', 'camn', 'cann', 'caon', 'capn', 'caqn', 'carn', 'casn', 'catn', 'caun', 'cavn', 'cawn', 'caxn', 'cayn', 'cazn'],
            },
        ]
        for test_case in test_cases:
            result = target(**test_case["input"])
            self.assertEqual(True, isinstance(result, list))
            self.assertEqual(len(result), len(test_case["expected"]))
            self.assertEqual(sorted(result), sorted(test_case["expected"]))

if __name__ == '__main__':
    unittest.main()
