import collections
import unittest

import numpy as np

from src.AutoCorrect import AutoCorrect


class AutoCorrectTest(unittest.TestCase):
    def test_process_data(self):
        auto_correct = AutoCorrect()
        target = auto_correct.process_data
        test_cases = [
            {
                "name": "default_check", "input": {"file_name": "/../../data/shakespeare.txt"},
                "expected": {
                    "expected_output_head": ["o", "for", "a", "muse", "of", "fire", "that", "would", "ascend", "the"],
                    "expected_output_tail": ['whilst', 'you', 'abide', 'here', 'enobarbus', 'humbly', 'sir', 'i', 'thank', 'you'],
                    "expected_n_words": 6205,
                },
            }
        ]
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
                    "expected_key_value_pairs": 6205,
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
            self.assertEqual(result.get("thee", 0), test_case["expected"]["expected_count_thee"])
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
                    "expected_prob_length": 6205,
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
                "expected": [
                    "aat",
                    "bat",
                    "cat",
                    "dat",
                    "eat",
                    "fat",
                    "gat",
                    "hat",
                    "iat",
                    "jat",
                    "kat",
                    "lat",
                    "mat",
                    "nat",
                    "oat",
                    "pat",
                    "qat",
                    "rat",
                    "sat",
                    "tat",
                    "uat",
                    "vat",
                    "wat",
                    "xat",
                    "yat",
                    "zat",
                    "aat",
                    "abt",
                    "act",
                    "adt",
                    "aet",
                    "aft",
                    "agt",
                    "aht",
                    "ait",
                    "ajt",
                    "akt",
                    "alt",
                    "amt",
                    "ant",
                    "aot",
                    "apt",
                    "aqt",
                    "art",
                    "ast",
                    "att",
                    "aut",
                    "avt",
                    "awt",
                    "axt",
                    "ayt",
                    "azt",
                    "ata",
                    "atb",
                    "atc",
                    "atd",
                    "ate",
                    "atf",
                    "atg",
                    "ath",
                    "ati",
                    "atj",
                    "atk",
                    "atl",
                    "atm",
                    "atn",
                    "ato",
                    "atp",
                    "atq",
                    "atr",
                    "ats",
                    "att",
                    "atu",
                    "atv",
                    "atw",
                    "atx",
                    "aty",
                    "atz",
                ],
            },
            {
                "name": "long_check",
                "input": {"word": "can"},
                "expected": [
                    "acan",
                    "bcan",
                    "ccan",
                    "dcan",
                    "ecan",
                    "fcan",
                    "gcan",
                    "hcan",
                    "ican",
                    "jcan",
                    "kcan",
                    "lcan",
                    "mcan",
                    "ncan",
                    "ocan",
                    "pcan",
                    "qcan",
                    "rcan",
                    "scan",
                    "tcan",
                    "ucan",
                    "vcan",
                    "wcan",
                    "xcan",
                    "ycan",
                    "zcan",
                    "caan",
                    "cban",
                    "ccan",
                    "cdan",
                    "cean",
                    "cfan",
                    "cgan",
                    "chan",
                    "cian",
                    "cjan",
                    "ckan",
                    "clan",
                    "cman",
                    "cnan",
                    "coan",
                    "cpan",
                    "cqan",
                    "cran",
                    "csan",
                    "ctan",
                    "cuan",
                    "cvan",
                    "cwan",
                    "cxan",
                    "cyan",
                    "czan",
                    "caan",
                    "cabn",
                    "cacn",
                    "cadn",
                    "caen",
                    "cafn",
                    "cagn",
                    "cahn",
                    "cain",
                    "cajn",
                    "cakn",
                    "caln",
                    "camn",
                    "cann",
                    "caon",
                    "capn",
                    "caqn",
                    "carn",
                    "casn",
                    "catn",
                    "caun",
                    "cavn",
                    "cawn",
                    "caxn",
                    "cayn",
                    "cazn",
                    "cana",
                    "canb",
                    "canc",
                    "cand",
                    "cane",
                    "canf",
                    "cang",
                    "canh",
                    "cani",
                    "canj",
                    "cank",
                    "canl",
                    "canm",
                    "cann",
                    "cano",
                    "canp",
                    "canq",
                    "canr",
                    "cans",
                    "cant",
                    "canu",
                    "canv",
                    "canw",
                    "canx",
                    "cany",
                    "canz",
                ],
            },
        ]
        for test_case in test_cases:
            result = target(**test_case["input"])
            self.assertEqual(True, isinstance(result, list))
            self.assertEqual(len(result), len(test_case["expected"]))
            self.assertEqual(sorted(result), sorted(test_case["expected"]))

    def test_edit_one_letter(self):
        auto_correct = AutoCorrect()
        target = auto_correct.edit_one_letter
        test_cases = [
        {
            "name": "default_check",
            "input": {"word": "at"},
            "expected": set(
                [
                    "a",
                    "aa",
                    "aat",
                    "ab",
                    "abt",
                    "ac",
                    "act",
                    "ad",
                    "adt",
                    "ae",
                    "aet",
                    "af",
                    "aft",
                    "ag",
                    "agt",
                    "ah",
                    "aht",
                    "ai",
                    "ait",
                    "aj",
                    "ajt",
                    "ak",
                    "akt",
                    "al",
                    "alt",
                    "am",
                    "amt",
                    "an",
                    "ant",
                    "ao",
                    "aot",
                    "ap",
                    "apt",
                    "aq",
                    "aqt",
                    "ar",
                    "art",
                    "as",
                    "ast",
                    "ata",
                    "atb",
                    "atc",
                    "atd",
                    "ate",
                    "atf",
                    "atg",
                    "ath",
                    "ati",
                    "atj",
                    "atk",
                    "atl",
                    "atm",
                    "atn",
                    "ato",
                    "atp",
                    "atq",
                    "atr",
                    "ats",
                    "att",
                    "atu",
                    "atv",
                    "atw",
                    "atx",
                    "aty",
                    "atz",
                    "au",
                    "aut",
                    "av",
                    "avt",
                    "aw",
                    "awt",
                    "ax",
                    "axt",
                    "ay",
                    "ayt",
                    "az",
                    "azt",
                    "bat",
                    "bt",
                    "cat",
                    "ct",
                    "dat",
                    "dt",
                    "eat",
                    "et",
                    "fat",
                    "ft",
                    "gat",
                    "gt",
                    "hat",
                    "ht",
                    "iat",
                    "it",
                    "jat",
                    "jt",
                    "kat",
                    "kt",
                    "lat",
                    "lt",
                    "mat",
                    "mt",
                    "nat",
                    "nt",
                    "oat",
                    "ot",
                    "pat",
                    "pt",
                    "qat",
                    "qt",
                    "rat",
                    "rt",
                    "sat",
                    "st",
                    "t",
                    "ta",
                    "tat",
                    "tt",
                    "uat",
                    "ut",
                    "vat",
                    "vt",
                    "wat",
                    "wt",
                    "xat",
                    "xt",
                    "yat",
                    "yt",
                    "zat",
                    "zt",
                ]
            ),
        },
        {
            "name": "long_check",
            "input": {"word": "can"},
            "expected": set(
                [
                    "aan",
                    "acan",
                    "acn",
                    "an",
                    "ban",
                    "bcan",
                    "ca",
                    "caa",
                    "caan",
                    "cab",
                    "cabn",
                    "cac",
                    "cacn",
                    "cad",
                    "cadn",
                    "cae",
                    "caen",
                    "caf",
                    "cafn",
                    "cag",
                    "cagn",
                    "cah",
                    "cahn",
                    "cai",
                    "cain",
                    "caj",
                    "cajn",
                    "cak",
                    "cakn",
                    "cal",
                    "caln",
                    "cam",
                    "camn",
                    "cana",
                    "canb",
                    "canc",
                    "cand",
                    "cane",
                    "canf",
                    "cang",
                    "canh",
                    "cani",
                    "canj",
                    "cank",
                    "canl",
                    "canm",
                    "cann",
                    "cano",
                    "canp",
                    "canq",
                    "canr",
                    "cans",
                    "cant",
                    "canu",
                    "canv",
                    "canw",
                    "canx",
                    "cany",
                    "canz",
                    "cao",
                    "caon",
                    "cap",
                    "capn",
                    "caq",
                    "caqn",
                    "car",
                    "carn",
                    "cas",
                    "casn",
                    "cat",
                    "catn",
                    "cau",
                    "caun",
                    "cav",
                    "cavn",
                    "caw",
                    "cawn",
                    "cax",
                    "caxn",
                    "cay",
                    "cayn",
                    "caz",
                    "cazn",
                    "cban",
                    "cbn",
                    "ccan",
                    "ccn",
                    "cdan",
                    "cdn",
                    "cean",
                    "cen",
                    "cfan",
                    "cfn",
                    "cgan",
                    "cgn",
                    "chan",
                    "chn",
                    "cian",
                    "cin",
                    "cjan",
                    "cjn",
                    "ckan",
                    "ckn",
                    "clan",
                    "cln",
                    "cman",
                    "cmn",
                    "cn",
                    "cna",
                    "cnan",
                    "cnn",
                    "coan",
                    "con",
                    "cpan",
                    "cpn",
                    "cqan",
                    "cqn",
                    "cran",
                    "crn",
                    "csan",
                    "csn",
                    "ctan",
                    "ctn",
                    "cuan",
                    "cun",
                    "cvan",
                    "cvn",
                    "cwan",
                    "cwn",
                    "cxan",
                    "cxn",
                    "cyan",
                    "cyn",
                    "czan",
                    "czn",
                    "dan",
                    "dcan",
                    "ean",
                    "ecan",
                    "fan",
                    "fcan",
                    "gan",
                    "gcan",
                    "han",
                    "hcan",
                    "ian",
                    "ican",
                    "jan",
                    "jcan",
                    "kan",
                    "kcan",
                    "lan",
                    "lcan",
                    "man",
                    "mcan",
                    "nan",
                    "ncan",
                    "oan",
                    "ocan",
                    "pan",
                    "pcan",
                    "qan",
                    "qcan",
                    "ran",
                    "rcan",
                    "san",
                    "scan",
                    "tan",
                    "tcan",
                    "uan",
                    "ucan",
                    "van",
                    "vcan",
                    "wan",
                    "wcan",
                    "xan",
                    "xcan",
                    "yan",
                    "ycan",
                    "zan",
                    "zcan",
                ]
            ),
        }]
        for test_case in test_cases:
            result = target(**test_case["input"])
            self.assertEqual(True, isinstance(result, set))
            self.assertEqual(len(result), len(test_case["expected"]))
            self.assertEqual(sorted(result), sorted(test_case["expected"]))

    def test_edit_two_letters(self):
        auto_correct = AutoCorrect()
        target = auto_correct.edit_two_letters
        test_cases = [
            {
                "name": "default_check1",
                "input": {"word": "a"},
                "expected": {
                    "expected_n_words_edit_dist": 2654,
                    "expected_head": [
                        "",
                        "a",
                        "aa",
                        "aaa",
                        "aab",
                        "aac",
                        "aad",
                        "aae",
                        "aaf",
                        "aag",
                    ],
                    "expected_tail": [
                        "zv",
                        "zva",
                        "zw",
                        "zwa",
                        "zx",
                        "zxa",
                        "zy",
                        "zya",
                        "zz",
                        "zza",
                    ],
                },
            },
            {
                "name": "default_check2",
                "input": {"word": "at"},
                "expected": {
                    "expected_n_words_edit_dist": 7154,
                    "expected_head": [
                        "",
                        "a",
                        "aa",
                        "aaa",
                        "aaat",
                        "aab",
                        "aabt",
                        "aac",
                        "aact",
                        "aad",
                    ],
                    "expected_tail": [
                        "zwt",
                        "zx",
                        "zxat",
                        "zxt",
                        "zy",
                        "zyat",
                        "zyt",
                        "zz",
                        "zzat",
                        "zzt",
                    ],
                },
            },
            {
                "name": "switches_check",
                "input": {"word": "at", "allow_switches": False},
                "expected": {
                    "expected_n_words_edit_dist": 7130,
                    "expected_head": [
                        "",
                        "a",
                        "aa",
                        "aaa",
                        "aaat",
                        "aab",
                        "aabt",
                        "aac",
                        "aact",
                        "aad",
                    ],
                    "expected_tail": [
                        "zwt",
                        "zx",
                        "zxat",
                        "zxt",
                        "zy",
                        "zyat",
                        "zyt",
                        "zz",
                        "zzat",
                        "zzt",
                    ],
                },
            },
            {
                "name": "long_check_no_switch",
                "input": {"word": "cat", "allow_switches": False},
                "expected": {
                    "expected_n_words_edit_dist": 14206,
                    "expected_head": [
                        "a",
                        "aa",
                        "aaa",
                        "aaat",
                        "aab",
                        "aabt",
                        "aac",
                        "aacat",
                        "aact",
                        "aad",
                    ],
                    "expected_tail": [
                        "zwt",
                        "zxat",
                        "zxcat",
                        "zxt",
                        "zyat",
                        "zycat",
                        "zyt",
                        "zzat",
                        "zzcat",
                        "zzt",
                    ],
                },
            },
            {
                "name": "long_check_no_switch",
                "input": {"word": "cat"},
                "expected": {
                    "expected_n_words_edit_dist": 14352,
                    "expected_head": [
                        "a",
                        "aa",
                        "aaa",
                        "aaat",
                        "aab",
                        "aabt",
                        "aac",
                        "aacat",
                        "aact",
                        "aad",
                    ],
                    "expected_tail": [
                        "zwt",
                        "zxat",
                        "zxcat",
                        "zxt",
                        "zyat",
                        "zycat",
                        "zyt",
                        "zzat",
                        "zzcat",
                        "zzt",
                    ],
                },
            },
        ]
        for test_case in test_cases:
            result = target(**test_case["input"])
            self.assertEqual(True, isinstance(result, set))
            self.assertEqual(len(result), test_case["expected"]["expected_n_words_edit_dist"])
            self.assertEqual(sorted(list(result))[:10], sorted(test_case["expected"]["expected_head"]))
            self.assertEqual(sorted(list(result))[-10:], sorted(test_case["expected"]["expected_tail"]))

    def test_get_corrections(self):
        auto_correct = AutoCorrect()
        target = auto_correct.get_corrections
        vocab = auto_correct.process_data('/../../data/shakespeare.txt')
        word_count_dict = auto_correct.get_count(vocab)
        probs = auto_correct.get_probs(word_count_dict)
        test_cases = [
            {
                "name": "default_check",
                "input": {"word": "dys", "probs": probs, "vocab": vocab, "n": 2},
                "expected": {
                    "n_best": [
                        ("days", 0.0004103405826836274),
                        ("dye", 1.865184466743761e-5),
                    ]
                },
            },
            {
                "name": "default_check",
                "input": {"word": "satr", "probs": probs, "vocab": vocab, "n": 2},
                "expected": {
                    "n_best": [
                        ("star", 0.00013056291267206328),
                        ("sat", 5.595553400231283e-05),
                    ]
                },
            },
            {
                "name": "default_check",
                "input": {"word": "san", "probs": probs, "vocab": vocab, "n": 5},
                "expected": {
                    "n_best": [
                        ("say", 0.0019770955347483865),
                        ("can", 0.0019211400007460738),
                        ("an", 0.0017719252434065728),
                        ("man", 0.0013242809713880702),
                        ("son", 0.0007274219420300668),
                    ]
                },
            },
        ]
        for test_case in test_cases:
            result = target(**test_case["input"])
            self.assertEqual(True, isinstance(result, list))
            self.assertEqual(True, len(result) == len(test_case["expected"]["n_best"]))
            for index, elem in enumerate(sorted(result)):
                self.assertEqual(True, elem[0] == sorted(test_case["expected"]["n_best"])[index][0])
                self.assertEqual(True, abs(elem[1] - sorted(test_case["expected"]["n_best"])[index][1]) < .01)

    def test_min_edit_distance(self):
        auto_correct = AutoCorrect()
        target = auto_correct.min_edit_distance
        test_cases = [
            {
                "name": "default_check1",
                "input": {
                    "source": "play",
                    "target": "stay",
                    "ins_cost": 1,
                    "del_cost": 1,
                    "rep_cost": 2,
                },
                "expected": {
                    "D": np.array(
                        [
                            [0, 1, 2, 3, 4],
                            [1, 2, 3, 4, 5],
                            [2, 3, 4, 5, 6],
                            [3, 4, 5, 4, 5],
                            [4, 5, 6, 5, 4],
                        ]
                    ),
                    "med": 4,
                },
            },
            {
                "name": "default_check2",
                "input": {
                    "source": "eer",
                    "target": "near",
                    "ins_cost": 1,
                    "del_cost": 1,
                    "rep_cost": 2,
                },
                "expected": {
                    "D": np.array(
                        [[0, 1, 2, 3, 4], [1, 2, 1, 2, 3], [2, 3, 2, 3, 4], [3, 4, 3, 4, 3]]
                    ),
                    "med": 3,
                },
            },
            {
                "name": "nonmodified_costs_check",
                "input": {
                    "source": "star",
                    "target": "stack",
                    "ins_cost": 1,
                    "del_cost": 1,
                    "rep_cost": 2,
                },
                "expected": {
                    "D": np.array(
                        [
                            [0, 1, 2, 3, 4, 5],
                            [1, 0, 1, 2, 3, 4],
                            [2, 1, 0, 1, 2, 3],
                            [3, 2, 1, 0, 1, 2],
                            [4, 3, 2, 1, 2, 3],
                        ]
                    ),
                    "med": 3,
                },
            },
            {
                "name": "modified_costs_check",
                "input": {
                    "source": "star",
                    "target": "stack",
                    "ins_cost": 2,
                    "del_cost": 2,
                    "rep_cost": 3,
                },
                "expected": {
                    "D": np.array(
                        [
                            [0, 2, 4, 6, 8, 10],
                            [2, 0, 2, 4, 6, 8],
                            [4, 2, 0, 2, 4, 6],
                            [6, 4, 2, 0, 2, 4],
                            [8, 6, 4, 2, 3, 5],
                        ]
                    ),
                    "med": 5,
                },
            },
        ]
        for test_case in test_cases:
            result = target(**test_case["input"])
            self.assertEqual(True, isinstance(result[0], type(result[0])))
            self.assertEqual(True, isinstance(result[1], type(result[1])))
            self.assertEqual(True, result[0].shape == test_case["expected"]["D"].shape)
            self.assertEqual(True, np.allclose(result[0], test_case["expected"]["D"]))
            self.assertEqual(True, np.isclose(result[1], test_case["expected"]["med"]))

if __name__ == '__main__':
    unittest.main()
