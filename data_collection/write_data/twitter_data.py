from tweepy import api
from .data_to_csv import DataToCSV
from .utility import create_logger, generate_data_stream
from ..api.twitter import get_tweets

def write_twitter_data(stock_symbols, result_type, query_type, file):
    """
    Write reddit posts data for given set of stock symbols to csv file

    Parameters:
        stock_symbols (set): set of stock symbols to get reddit data for
        result_type (str): type of tweets to get, either 'mixed' or 'popular'
        query_type (str): type of query to search twitter api with, either
        'mixed' or 'financial'
        file (str): csv file to write to
    
    Raises:
        ValueError if query or result type is not supported
    """
    # Check if query_type and result_type are of the supported values
    supported_query_type = {"mixed", "financial"}
    supported_result_type = {"mixed", "popular"}
    if (query_type not in supported_query_type) or (result_type not in supported_result_type):
        raise ValueError("Invalid query or result type")

    logger = create_logger(__name__)
    # Twitter data consist of id, date, symbol and tweet, and are considered
    # duplicates if id of tweets are the same
    field_names = ["id", "date", "symbol", "tweet"]
    unique_identifiers = ["id"]

    try:
        data_to_csv = DataToCSV(file=file, field_names=field_names, unique_identifiers=unique_identifiers)
        # Use lambda expression for api_call which takes in a unary function that accepts a symbol
        # Get 15 tweets per symbol, and add no delay as tweepy api automatically waits on rate limit
        api_call = lambda symbol: get_tweets(symbol=symbol, query_type=query_type, result_type=result_type, n_items=15)
        data_stream = generate_data_stream(stock_symbols=stock_symbols, api_call=api_call, delay=0)
        rows_written = data_to_csv.write(data_stream)
        logger.info(f"{rows_written} rows written to {file}")
    except AttributeError:
        logger.error("Invalid field names or csv file headers")