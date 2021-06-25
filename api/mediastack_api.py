import http.client, urllib.parse
from os import getenv
from datetime import datetime, timedelta
from api.article import Article
import json


# Set up connection with base url of mediastack API
conn = http.client.HTTPConnection('api.mediastack.com')
api_key = getenv("NEWS_API_KEY")

# We will fix the query for news article to be at most 1 week old
TODAY = datetime.now()
WEEK_AGO = TODAY - timedelta(days=7)

def get_financial_news(symbol, n_items):
    """Get financial news of given symbol.

    Get up to n_items number of financial news from the past 7 days 
    for given stock symbol, by querying the mediastack API 
    with the symbol name. 

    Args:
        symbol (str): Symbol of stock to query tweets for
        n_items (int): Max number of news to return per query

    Yields:
        Article object which contains the title, published date and 
        description of the news article, the symbol the article is associated
        with, and the url to the original article

    """
    search_params = urllib.parse.urlencode({
            'access_key': api_key,
            'limit': n_items,
            'keywords': symbol,
            'date': f"{WEEK_AGO.strftime('%Y-%m-%d')},{TODAY.strftime('%Y-%m-%d')}",
            'languages': 'en',
            'sort': 'published_desc'
        })

    conn.request('GET', '/v1/news?{}'.format(search_params))
    response = conn.getresponse()
    data = response.read()
    news_articles = json.loads(data)['data']

    for article in news_articles:
        yield Article(title=article['title'], description=article['description'],
                      date=article['published_at'].split("T")[0], symbol=symbol, url=article['url'])
