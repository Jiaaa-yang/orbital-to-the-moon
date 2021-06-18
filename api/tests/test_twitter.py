import unittest
from api import twitter_api


class TestTwitterAPI(unittest.TestCase):

    def test_returned_dictionary_keys(self):
        # Use arbitrary symbols, result_type and n_items
        tweets = twitter_api.get_financial_tweets("MSFT", "mixed", 3)
        tweet_keys = next(tweets).keys()
        expected_keys = {'id', 'date', 'symbol', 'tweet'}
        self.assertEqual(set(tweet_keys), expected_keys)


if __name__ == '__main__':
    unittest.main()
