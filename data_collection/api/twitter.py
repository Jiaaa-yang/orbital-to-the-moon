import tweepy
from os import getenv

CONSUMER_KEY = getenv("TWITTER_CONSUMER_KEY")
CONSUMER_SECRET = getenv("TWITTER_CONSUMER_SECRET")
ACCESS_TOKEN = getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Tweepy authentication
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

def get_financial_tweets(symbol, result_type, n_items):
    """Get financial tweets of given symbol.

    Get up to n_items number of financial tweets for given symbol,
    separated by result_type, which can be 'popular' which fetches 
    popular tweets only, or 'mixed' which fetches both popular and
    recently posted tweets.

    Args:
        symbol (str): Symbol of stock to query tweets for
        result_type (str): Type of tweets to query for: either 'popular' or 'mixed'
        n_items (int): Max number of tweets to return per query

    Yields:
        dict: Tweets with the following keys:
        'id': id of tweet
        'date': date where tweet was created, in YYYY-MM-DD format
        'symbol': stock symbol associated with tweet returned
        'tweet': text of tweet retrieved

    Raises:
        ValueError: If result_type is not 'mixed' or 'popular'

    """
    result_type = result_type.lower()
    supported_result_types = {"mixed", "popular"}
    if result_type not in supported_result_types:
        raise ValueError("Invalid result type")

    # Query for twitter API to be symbol prepended with a '$' sign to get financial tweets
    query = f"${symbol} -filter:retweets"
    tweets = tweepy.Cursor(api.search, q=query, lang="en", result_type=result_type, tweet_mode="extended").items(n_items)
    for tweet in tweets:
        yield {'id': tweet.id,
               'date': tweet.created_at.strftime("%Y-%m-%d"),
               'symbol': symbol,
               'tweet': tweet.full_text}
