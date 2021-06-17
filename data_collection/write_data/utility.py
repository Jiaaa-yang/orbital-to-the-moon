import logging
import time

def create_logger(name, filename='data_collection.log'):
    """Create a logger instance to log to log files.

    Utility function to instantiate logger to allow different
    functions to create their own instance and log to the same
    file in the same format.

    Args:
        name (str): Name of logger to instantiate
        filename (str, optional): File to log data to,
            defaults to 'data_collection.log'

    Returns:
        Logger object to log to given file

    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(filename=filename)
    formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def generate_data_stream(stock_symbols, api_call, delay):
    """Get data stream from api calls.

    Utility function to generate data stream by passing
    each symbol in stock_symbols to the api_call which takes in
    a single symbol as parameter and returns the appropriate data.

    Args:
        stock_symbols (set): Set of stock symbols to generate data for
        api_call (function): Unary function which takes in a single stock
            symbol and yields the required data from the api_calls
        delay (int): Time delay to add between each call to adhere to rate limits

    Yields:
        dict: Data stream consisting of data returned by api calls for
            every stock ticker in stock_symbols        

    """
    symbols_processed = 0
    for stock in stock_symbols:
        generator = api_call(stock)
        for data in generator:
            yield data
        time.sleep(delay)
        # Progress tracking for every 25 symbols processed
        symbols_processed += 1
        if symbols_processed % 25 == 0:
            print(f"{symbols_processed} symbols have been processed")