import unittest
from api import alpha_vantage_api
from datetime import datetime


class TestAlphaVantageAPI(unittest.TestCase):

    def setUp(self):
        # Get prices data for arbitrary stock symbol
        self.test_symbol = "MSFT"
        self.data = alpha_vantage_api.get_daily_price(self.test_symbol)


    def test_returned_dictionary_keys(self):
        price_data_keys = next(self.data).keys()
        expected_keys = {'date', 'symbol', 'adjusted_close'}
        self.assertEqual(set(price_data_keys), expected_keys)


    def test_correct_date_format(self):
        # Test for YYYY-MM-DD format for date field in dictionary returned
        for price_data in self.data:
            date = price_data['date']
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                self.fail("Date passed in is not in YYYY-MM-DD format")
                

    def test_correct_symbol(self):
        price_data = next(self.data)
        price_data_symbol = price_data['symbol']
        self.assertEqual(price_data_symbol, self.test_symbol)
