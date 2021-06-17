from alpha_vantage.timeseries import TimeSeries
from os import getenv

api = TimeSeries(getenv("ALPHAVANTAGE_API_KEY"))

def get_daily_price(symbol):
    """Get prices data for given symbol.

    Get daily adjusted closing price data for given symbol
    using AlphaVantage API, for up to past 100 data points.

    Args:
        symbol (str): Symbol of stock to get prices data for

    Yields:
        dict: Price data with the following keys:
        'date': date associated with current data
        'symbol': symbol associated with current data
        'adjusted_close': adjusted closing price of given symbol on given date

    """
    prices_data, _ = api.get_daily_adjusted(symbol=symbol, outputsize="compact")
    for key, value in prices_data.items():
        yield {"date": key,
               "symbol": symbol,
               "adjusted_close": value['5. adjusted close']}