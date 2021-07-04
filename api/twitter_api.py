import tweepy
from api.tweet import Tweet
from datetime import datetime
from os import getenv


CONSUMER_KEY = getenv("TWITTER_CONSUMER_KEY")
CONSUMER_SECRET = getenv("TWITTER_CONSUMER_SECRET")
ACCESS_TOKEN = getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = getenv("TWITTER_ACCESS_TOKEN_SECRET")
TODAY = datetime.now()

# Tweepy authentication
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

def get_financial_tweets(symbol, result_type, n_items, date_range="all"):
    """Get financial tweets of given symbol.

    Get up to n_items number of financial tweets for given symbol,
    separated by result_type, which can be 'popular' which fetches 
    popular tweets only, or 'mixed' which fetches both popular and
    recently posted tweets. Users can also specify the date range to get
    tweets from, either 'all' which fetches tweets from the past 7 days,
    or 'today' which only fetches tweets on current day.

    Args:
        symbol (str): Symbol of stock to query tweets for
        result_type (str): Type of tweets to query for: either 'popular' or 'mixed'
        n_items (int): Max number of tweets to return per query
        date_range (str, optional): Date range of tweets to query: either
            'all' or 'today'. Defaults to 'all'

    Yields:
        Tweet object which contains the tweet id, date of tweet, symbol
            the tweet is associated with, and the text content
    """
    # Query for twitter API to be symbol prepended with a '$' sign to get financial tweets
    query = f"${symbol} -filter:retweets"
    if date_range == "all":
        tweets = tweepy.Cursor(api.search, q=query, lang="en", result_type=result_type, 
                               tweet_mode="extended").items(n_items)
    else:
        tweets = tweepy.Cursor(api.search, q=query, lang="en", result_type=result_type, 
                               since=TODAY.strftime("%Y-%m-%d"), tweet_mode="extended").items(n_items)

    for tweet in tweets:
        yield Tweet(id=tweet.id, date=tweet.created_at.strftime("%Y-%m-%d"), symbol=symbol, text=tweet.full_text)
