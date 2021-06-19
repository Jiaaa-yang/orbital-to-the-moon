import unittest
from api import twitter_api
from datetime import datetime


class TestTwitterAPI(unittest.TestCase):

    def setUp(self):
        # Get twitter data for arbitrary stock symbol and result types
        self.test_symbol = "MSFT"
        self.data = twitter_api.get_financial_tweets(symbol=self.test_symbol, result_type="mixed", n_items=3)


    def test_returned_dictionary_keys(self):
        tweet_keys = next(self.data).keys()
        expected_keys = {'id', 'date', 'symbol', 'tweet'}
        self.assertEqual(set(tweet_keys), expected_keys)


    def test_correct_date_format(self):
        # Test for YYYY-MM-DD format for date field in dictionary returned
        for tweet in self.data:
            date = tweet['date']
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                self.fail("Date passed in is not in YYYY-MM-DD format")


    def test_correct_symbol(self):
        tweet = next(self.data)
        tweet_symbol = tweet['symbol']
        self.assertEqual(tweet_symbol, self.test_symbol)
    

    def test_non_empty_text_field(self):
        tweet = next(self.data)
        tweet_text_content = tweet['tweet']
        self.assertTrue(tweet_text_content)
