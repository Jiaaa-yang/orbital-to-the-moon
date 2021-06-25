import unittest
from ..tweets_analysis import analyse_symbol


class TestTweetsAnalysis(unittest.TestCase):

    def setUp(self):
        self.test_symbol = "MSFT"
        self.analysis = analyse_symbol(self.test_symbol)


    def test_analyse_symbols_returns_dictionary(self):
        self.assertIsInstance(self.analysis, dict)


    def test_analyse_symbols_is_bullish_is_bool(self):
        is_bullish = self.analysis['is_bullish']
        self.assertIsInstance(is_bullish, bool)


    def test_analyse_symbols_has_correct_dictionary_keys(self):
        actual_keys = set(self.analysis.keys())
        expected_keys = {'is_bullish', 'confidence_level', 'bullish_tweets', 'bearish_tweets'}
        self.assertEqual(actual_keys, expected_keys)
