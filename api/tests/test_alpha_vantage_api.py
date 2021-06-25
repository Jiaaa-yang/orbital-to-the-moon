import unittest
from api import alpha_vantage_api
from datetime import datetime


class TestAlphaVantageAPI(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # Get prices data for arbitrary stock symbol with one API call
        self.test_symbol = "MSFT"
        self.data = list(alpha_vantage_api.get_daily_price(self.test_symbol))


    def test_get_daily_prices_return_dictionary_with_expected_keys(self):
        expected_keys = {'date', 'symbol', 'adjusted_close'}
        for data in self.data:
            actual_keys = set(data.keys())
            self.assertEqual(actual_keys, expected_keys)


    def test_get_daily_prices_return_date_in_YYYY_MM_DD_format(self):
        for price_data in self.data:
            date = price_data['date']
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                self.fail("Date is not in YYYY-MM-DD format")
                

    def test_get_daily_prices_return_prices_for_correct_symbol(self):
        for data in self.data:
            actual_symbol = data['symbol']
            self.assertEqual(actual_symbol, self.test_symbol)
