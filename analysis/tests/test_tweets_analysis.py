import unittest
from ..tweets_analysis import analyse_symbol

class TestTweetsAnalysis(unittest.TestCase):

    def setUp(self):
        self.test_symbol = "MSFT"
        self.analysis = analyse_symbol(self.test_symbol)


    def test_analyse_symbols_price_rise_is_boolean(self):
        price_rise = self.analysis['price_rise']
        self.assertIsInstance(price_rise, bool)


    def test_analyse_symbols_bullish_tweets_dictionary_keys(self):
        bullish_tweets = self.analysis['bullish_tweets']
        expected_keys = {'id', 'date', 'symbol', 'tweet'}
        for tweet in bullish_tweets:
            actual_keys = set(tweet.keys())
            self.assertEqual(actual_keys, expected_keys)
