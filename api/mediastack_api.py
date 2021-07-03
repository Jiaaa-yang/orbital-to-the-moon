from json.decoder import JSONDecodeError
from os import getenv
import requests
from datetime import datetime, timedelta
from api.article import Article


# Define base url for accessing news articles from mediastack api
news_access_url = "http://api.mediastack.com/v1/news"
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

    Returns:
        List of Article objects which contains the title, published date and 
        description of the news article, the symbol the article is associated
        with, and the url to the original article

    """
    search_params = {
            'access_key': api_key,
            'limit': n_items,
            'keywords': symbol,
            'date': f"{WEEK_AGO.strftime('%Y-%m-%d')},{TODAY.strftime('%Y-%m-%d')}",
            'languages': 'en',
            'sort': 'published_desc'
        }

    response = requests.get(news_access_url, params=search_params)
    try:
        response_data = response.json()
    except JSONDecodeError:
        # Check for valid JSON response as mediastack API may return
        # invalid JSON format occasionally
        return []


    if 'error' in response_data:
        # Mediastack returns a dictionary with a single 'error' key 
        # when an API request is unsuccessful. 
        return []

    results = []
    news_articles = response_data['data']
    for article in news_articles:
        results.append(Article(title=article['title'], description=article['description'],
                      date=article['published_at'].split("T")[0], symbol=symbol, url=article['url']))

    return results
