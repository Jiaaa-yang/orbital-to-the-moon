import unittest
from api import twitter_api, tweet
from datetime import datetime


class TestTwitterAPI(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # Get arbitrary twitter data for one single API call to use for test cases
        self.test_symbol = "MSFT"
        self.data = list(twitter_api.get_financial_tweets(symbol=self.test_symbol, result_type="mixed", n_items=3))


    def test_get_financial_tweets_return_list_of_tweet_objects(self):
        for data in self.data:
            self.assertIsInstance(data, tweet.Tweet)


    def test_get_financial_tweets_returned_tweets_has_date_in_YYYY_MM_DD_format(self):
        for tweet in self.data:
            date = tweet.date
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                self.fail("Date is not in YYYY-MM-DD format")


    def test_get_financial_tweets_returned_tweets_has_correct_symbol(self):
        for tweet in self.data:
            self.assertEqual(tweet.symbol, self.test_symbol)
