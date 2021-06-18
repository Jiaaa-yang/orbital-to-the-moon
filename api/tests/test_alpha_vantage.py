import unittest
from api import alpha_vantage_api


class TestAlphaVantageAPI(unittest.TestCase):

    def test_returned_dictionary_keys(self):
        prices_data = alpha_vantage_api.get_daily_price("MSFT")
        price_data_keys = next(prices_data).keys()
        expected_keys = {'date', 'symbol', 'adjusted_close'}
        self.assertEqual(set(price_data_keys), expected_keys)


if __name__ == '__main__':
    unittest.main()