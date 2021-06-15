import logging
import time

def create_logger(name, filename='data_collection.log'):
    """
    Utility function to instantiate logger to log data written
    in the same format

    Parameters:
        name (str): name of logger to instantiate
        filename (str), optional: file to log data to

    Returns:
        Logger object for logging of data written
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(filename=filename)
    formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def generate_data_stream(stock_symbols, api_call, delay):
    """
    Utility function to generate data stream using the api

    Parameters:
        stock_symbols (set): set of stock symbols to generate data for
        api_call (function): unary function which takes in a single stock
        symbol and yields the required data from the api_calls
        delay (int): time delay to add to adhere to api rate limits

    Yields:
        Data stream consisting of data returned by api calls for
        every stock ticker in stock_symbols        
    """
    symbols_processed = 0
    for stock in stock_symbols:
        generator = api_call(stock)
        for data in generator:
            yield data
        time.sleep(delay)
        # Progress tracking for every 25 symbols processed for self use
        symbols_processed += 1
        if symbols_processed % 25 == 0:
            print(f"{symbols_processed} symbols have been processed")