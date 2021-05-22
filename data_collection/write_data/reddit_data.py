from .data_to_csv import DataToCSV
from .utility import create_logger, generate_data_stream
from ..api.reddit import get_stocks_posts

def write_reddit_data(stock_symbols, file="reddit_posts.csv"):
    """
    Write reddit posts data for given set of stock symbols to csv file

    Parameters:
        stock_symbols (set): set of stock symbols to get reddit data for
        file (str), optional: csv file to write to
    """
    logger = create_logger(__name__)
    # Reddit data consist of id, timestamp, symbol and text data, and are considered
    # duplicates if id of posts are the same
    field_names = ["id", "unix_timestamp_utc", "symbol", "text"]
    unique_identifiers = ["id"]

    try:
        data_to_csv = DataToCSV(file=file, field_names=field_names, unique_identifiers=unique_identifiers)
        # Reddit api has no rate limit, but include a 0.5s delay for courtesy
        data_stream = generate_data_stream(stock_symbols=stock_symbols, api_call=get_stocks_posts, delay=0.5)
        rows_written = data_to_csv.write(data_stream)
        logger.info(f"{rows_written} rows written to reddit_posts.csv")
    except AttributeError:
        logger.error("Invalid field names or csv file headers")