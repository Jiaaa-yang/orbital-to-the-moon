import unittest
from api import mediastack_api, article
from datetime import datetime


class TestMediastackAPI(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # Get arbitrary news data for one single API call to use for test cases
        self.test_symbol = "MSFT"
        self.data = mediastack_api.get_financial_news(symbol=self.test_symbol, n_items=3)


    def test_get_financial_news_return_list_of_article_objects(self):
        for data in self.data:
            self.assertIsInstance(data, article.Article)


    def test_get_financial_news_returned_article_has_date_in_YYYY_MM_DD_format(self):
        for article in self.data:
            date = article.date
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                self.fail("Date is not in YYYY-MM-DD format")
