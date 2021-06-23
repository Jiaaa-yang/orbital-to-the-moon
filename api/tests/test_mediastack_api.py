import unittest
from api import mediastack_api
from datetime import datetime


class TestMediastackAPI(unittest.TestCase):

    def setUp(self):
        # Get financial news data for arbitrary stock symbol and result types
        self.test_symbol = "MSFT"
        self.data = mediastack_api.get_financial_news(symbol=self.test_symbol, n_items=3)


    def test_returned_dictionary_keys(self):
        tweet_keys = next(self.data).keys()
        expected_keys = {'title', 'description', 'date', 'symbol', 'url'}
        self.assertEqual(set(tweet_keys), expected_keys)


    def test_correct_date_format(self):
        # Test for YYYY-MM-DD format for date field in dictionary returned
        for article in self.data:
            date = article['date']
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                self.fail("Date is not in YYYY-MM-DD format")
