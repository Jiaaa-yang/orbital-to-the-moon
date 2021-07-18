import unittest
from api.tweet import Tweet
from ..cache import get_cached_analysis, add_symbol_analysis, cache


class TestModels(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # Insert arbitrary data into the cache database for testing purposes
        self.test_symbol = "VALID_SYMBOl"
        self.invalid_symbol = "INVALID_SYMBOL"
        self.result = {
            'is_bullish': True,
            'confidence_level': 0,
            'bullish_tweets': [Tweet(id="0", date="2000-01-01", symbol=self.test_symbol, text="test text", likes=0)],
            'bearish_tweets': [Tweet(id="0", date="2000-01-01", symbol=self.test_symbol, text="test text", likes=0)]
        }


    @classmethod
    def tearDownClass(self):
        cache.delete_one({'symbol': self.test_symbol})


    def test_get_cached_analysis_returns_tuple(self):
        result = get_cached_analysis(self.test_symbol)
        self.assertIsInstance(result, tuple)


    def test_get_cached_analysis_returns_false_in_tuple_for_invalid_symbol(self):
        valid_cache, _ = get_cached_analysis(self.invalid_symbol)
        self.assertFalse(valid_cache)


    def test_add_symbol_analysis_returns_valid_cache_when_getting_cached_analysis(self):
        add_symbol_analysis(self.test_symbol, self.result)
        valid_cache, _ = get_cached_analysis(self.test_symbol)
        self.assertTrue(valid_cache)
