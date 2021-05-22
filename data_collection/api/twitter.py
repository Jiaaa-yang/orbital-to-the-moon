import tweepy
import yfinance as yf
from os import getenv

CONSUMER_KEY = getenv("TWITTER_CONSUMER_KEY")
CONSUMER_SECRET = getenv("TWITTER_CONSUMER_SECRET")
ACCESS_TOKEN = getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Tweepy authentication
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

def get_tweets(symbol, query_type, result_type, n_items):
    """
    Get tweets based on symbol, query and result type

    Parameters:
        symbol (str): symbol of stock to query tweets for
        query_type (str): type of query to query tweets for: either 'financial' or 'mixed',
        where the first gets mainly financial tweets, and mixed gets a mix of both financial 
        and information tweets
        result_type (str): type of tweets to query for: either 'popular' or 'mixed', 
        where the first gets popular tweets, and mixed gets a mix of both popular and recent tweets
        n_items (int): max number of items to return per query

    Yields:
        Tweets in dictionary form with following keys:
        'id': id of tweet
        'date': date where tweet was created, in YYYY-MM-DD format
        'symbol': stock symbol associated with tweet returned
        'tweet': text of tweet retrieved
    """
    # Check if query_type and result_type are of the supported values
    supported_query_type = {"mixed", "financial"}
    supported_result_type = {"mixed", "popular"}
    if (query_type not in supported_query_type) or (result_type not in supported_result_type):
        raise ValueError("Invalid query or result type")

    query = get_twitter_query(symbol, query_type)
    tweets = tweepy.Cursor(api.search, q=query, lang="en", result_type=result_type, tweet_mode="extended").items(n_items)
    for tweet in tweets:
        yield {'id': tweet.id,
               'date': tweet.created_at.strftime("%Y-%m-%d"),
               'symbol': symbol,
               'tweet': tweet.full_text}


def get_twitter_query(symbol, query_type):
    """
    Get a twitter query for given symbol and query type,
    based on twitter api: 
    https://developer.twitter.com/en/docs/labs/recent-search/guides/search-queries

    Parameters:
        symbol (str): symbol of stock to build query for
        query_type (str): type of query to build: either one of 'financial' or 'mixed'.
        The first will build a query by merely appending a $ sign, while 'mixed' includes
        company name of stock, and tweets with its hashtag

    Returns:
        string representing the query to be used for the search API
    """
    query_type = query_type.lower()
    if query_type == "financial":
        return f'${symbol} -filter:retweets'
    else:
        stock = yf.Ticker(symbol)
        company_name = stock.info['shortName']
        return f'("{company_name}" OR {symbol}) (${symbol} OR #{symbol}) -filter:retweets'