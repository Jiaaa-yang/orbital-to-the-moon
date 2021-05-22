import praw
from os import getenv

# Reddit api authentication
api = praw.Reddit(
    client_id=getenv("REDDIT_CLIENT_ID"),
    client_secret=getenv("REDDIT_CLIENT_SECRET"),
    user_agent=getenv("REDDIT_USER_AGENT")
)

def get_stocks_posts(symbol):
    """
    Get reddit submissions based on stock symbol

    Parameters:
        symbol (str): symbol of stock to query tweets for

    Yields:
        Reddit submissions in dictionary form with following keys:
        'id': id of reddit submission
        'unix_timestamp_utc': utc unix timestamp of submission
        'symbol': stock symbol associated with submission returned
        'text': text content of submission retrieved
    """
    # Search r/Stocks and r/Wallstreetbets subreddits only, separated by '+'
    stocks_subreddit = api.subreddit("stocks+wallstreetbets")

    query = f"${symbol}"
    for submission in stocks_subreddit.search(query=query, sort="hot", time_filter="week"):
        yield {"id": submission.id,
               "unix_timestamp_utc": submission.created_utc,
               "symbol": symbol,
               "text": submission.selftext
        }