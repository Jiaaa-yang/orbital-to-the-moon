from .data_to_csv import DataToCSV
from .utility import create_logger, generate_data_stream
from ..api.alpha_vantage import get_daily_price

def write_prices_data(stock_symbols, file="prices_data.csv"):
    """
    Write prices data for given set of stock symbols to csv file

    Parameters:
        stock_symbols (set): set of stock symbols to get prices data for
        file (str), optional: csv file to write to
    """
    logger = create_logger(__name__)
    # Prices data consist of date, symbol and adjusted close, and are considered
    # duplicates only if both date and symbol are the same
    field_names = ["date", "symbol", "adjusted_close"]
    unique_identifiers = ["date", "symbol"]

    try:
        data_to_csv = DataToCSV(file=file, field_names=field_names, unique_identifiers=unique_identifiers)
        # Alpha vantage has a rate limit of 5 api calls per minute, so delay each api call by 12 seconds
        data_stream = generate_data_stream(stock_symbols=stock_symbols, api_call=get_daily_price, delay=12)
        rows_written = data_to_csv.write(data_stream)
        logger.info(f"{rows_written} rows written to prices_data.csv")
    except ValueError:
        logger.error("Rate limit for alpha vantage exceeded. prices_data.csv not updated")
    except AttributeError:
        logger.error("Invalid field names or csv file headers")
