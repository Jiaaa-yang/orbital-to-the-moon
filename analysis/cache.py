import pymongo
from os import getenv
from copy import deepcopy
from pymongo import MongoClient
from datetime import datetime, timedelta
from api.tweet import Tweet


client = MongoClient(getenv("MONGODB_URI"))
cache = client.orbital.cache

def add_symbol_analysis(symbol, result):
    """Adds the result of a stock symbol analysis to cache

    Stores the result of analysing a given stock symbol into a
    MongoDB collection to act as a cache. List of tweet objects
    will converted into a dictionary of its attributes. A timestamp
    will also be added for reference of the recency of the stored results.

    Args:
        symbol (str): Ticker symbol of stock result is associated with
        result (dict): Dictionary with the following keys:
            'is_bullish': boolean stating whether the model predicts
                whether the sentiment of the stock is bullish
            'confidence_level': confidence level for prediction
            'bullish_tweets': list of top bullish Tweet objects predicted by model
            'bearish_tweets': list of top bearish Tweet objects predicted by model

    """
    result = deepcopy(result)
    current_time = datetime.now()
    result['time'] = current_time

    result['symbol'] = symbol
    # Convert each Tweet object into its dictionary form of attributes for storage
    result['bullish_tweets'] = [vars(tweet) for tweet in result['bullish_tweets']]
    result['bearish_tweets'] = [vars(tweet) for tweet in result['bearish_tweets']]

    cache.insert_one(result)


def get_cached_analysis(symbol):
    """Fetch the cached analysis result of the given symbol

    Fetches the result of analysing a given stock symbol from the
    MongoDB collection if it exists and if the timestamp of the result
    is no older than a given threshold from the current time. If the result
    exists in the database and is too old, it will also be deleted.

    Args:
        symbol (str): Ticker symbol of stock to get analysis results for

    Returns:
        tuple: Tuple of 2 elements. The first is a boolean indicating whether there
            exists a valid result in the cache database. The second is the result
            in a dictionary form with the following keys:
                'is_bullish': boolean stating whether the model predicts
                    whether the sentiment of the stock is bullish
                'confidence_level': confidence level for prediction
                'bullish_tweets': list of top bullish Tweet objects predicted by model
                'bearish_tweets': list of top bearish Tweet objects predicted by model

    """
    # Define the threshold to be 3600 in seconds, hence any result that is more than 1 hour
    # old from the current time is considered to be invalid
    threshold = 60 * 60

    result = cache.find_one({'symbol': symbol})
    if result == None:
        # Analysis of given symbol does not exist in cache
        return False, result

    result_time = result['time']
    current_time = datetime.now()
    if (current_time - result_time).total_seconds() > threshold:
        # Previous analysis was too long ago, delete result and return invalid result
        cache.delete_one({'_id': result['_id']})
        return False, result

    # Valid result in cache, return the result in the desired form by removing
    # unncessary fields and converting tweet attributes back into Tweet object
    del result['time']
    del result['_id']
    del result['symbol']
    result['bullish_tweets'] = [Tweet(**attributes) for attributes in result['bullish_tweets']]
    result['bearish_tweets'] = [Tweet(**attributes) for attributes in result['bearish_tweets']]
    return True, result


def get_recommended_stocks():
    """Gets recommended stocks from the cache

    Query recommended stocks from the cache, which is defined as those
    with a bullish prediction and is not older than 1 day ago. Also sorts
    them by confidence level of the prediction such that the most
    confident bullish prediction is first in the returned list 

    Returns:
        list: List of sorted dictionary with the following keys:
            'symbol': symbol of stock of corresponding analysis result
            'confidence_level': confidence level of the prediction
            'datetime': datetime of this prediction, in DD-MM-YYYY HH:MM format

    """
    one_day_ago = datetime.now() - timedelta(days=1)
    bullish_stocks = cache.find({'is_bullish': True, 'time': {"$gt": one_day_ago}}).sort('confidence_level', pymongo.DESCENDING)
    recommended_stocks = []
    for stock in bullish_stocks:
        result = {
            'symbol': stock['symbol'],
            'confidence_level': "{:.2f}".format(stock['confidence_level']),
            'datetime': (stock['time'] + timedelta(hours=8)).strftime("%d-%m-%Y %H:%M")
        }
        recommended_stocks.append(result)

    # Return up to top ten bullish stocks
    return recommended_stocks[:10]
