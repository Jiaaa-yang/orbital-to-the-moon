from .data_to_csv import DataToCSV
from .utility import create_logger, generate_data_stream
from ..api.twitter import get_financial_tweets

def write_twitter_data(stock_symbols, result_type, file):
    """Write twitter data for given set of symbols.

    Write twitter data for every symbol in given set of 
    stock_symbols into the given csv file. Twitter data can be 
    separated by result_type, which can be 'popular' which fetches 
    popular tweets only, or 'mixed' which fetches both popular and
    recently posted tweets.
    
    Parameters:
        stock_symbols (set): Set of stock symbols to get twitter data for
        result_type (str): Type of tweets to get, either 'mixed' or 'popular'
        file (str): csv file to write to
    
    Raises:
        ValueError: If result_type is not 'popular' or 'mixed'

    """
    result_type = result_type.lower()
    supported_result_type = {"mixed", "popular"}
    if result_type not in supported_result_type:
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
        api_call = lambda symbol: get_financial_tweets(symbol=symbol, result_type=result_type, n_items=15)
        data_stream = generate_data_stream(stock_symbols=stock_symbols, api_call=api_call, delay=0)
        rows_written = data_to_csv.write(data_stream)
        logger.info(f"{rows_written} rows written to {file}")
    except AttributeError:
        logger.error("Invalid field names or csv file headers")
