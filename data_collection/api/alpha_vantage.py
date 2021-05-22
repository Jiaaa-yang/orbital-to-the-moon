from alpha_vantage.timeseries import TimeSeries
from os import getenv

api = TimeSeries(getenv("ALPHAVANTAGE_API_KEY"))

def get_daily_price(symbol):
    """
    Get prices data for given symbol, for up to past 100 data points

    Parameters:
        symbol (str): symbol of stock to query tweets for

    Yields:
        Price data in dictionary form with following keys:
        'date': date associated with current data
        'symbol': symbol associated with current data
        'adjusted_close': adjusted closing price of given symbol on given date
    """
    prices_data, _ = api.get_daily_adjusted(symbol=symbol, outputsize="compact")
    for key, value in prices_data.items():
        yield {"date": key,
               "symbol": symbol,
               "adjusted_close": value['5. adjusted close']}