from analysis.tweets_analysis import analyse_symbol
from api.mediastack_api import get_financial_news
from flask import (
    Blueprint, redirect, render_template, flash
)
import yfinance as yf


bp = Blueprint('analysis', __name__)

@bp.route('/analysis')
def analysis(symbol):
    symbol = symbol.upper()
    stock_info = yf.Ticker(symbol).info
    
    if len(stock_info) == 1:
        # Stock does not exist from lookup on Yahoo Finance
        flash('No matching company listing found')
        return redirect('/')

    analysis = analyse_symbol(symbol)

    company_name = stock_info['shortName']
    price_movement_prediction = "RISE" if analysis['is_bullish'] else "FALL"
    confidence_level = "{:.2f}".format(analysis['confidence_level'])
    bullish_tweets = analysis['bullish_tweets']
    bearish_tweets = analysis['bearish_tweets']

    # Get up to 5 items to display for each section and pass them
    # as a list of dictionary with relevant data
    n_display = 5
    bullish_tweets_display = []
    bearish_tweets_display = []

    for i in range(min(n_display, len(bullish_tweets))):
        tweet = bullish_tweets[i]
        bullish_tweets_display.append({'text': tweet.get_truncated_text(),
                                       'link': tweet.get_link()})

    for i in range(min(n_display, len(bearish_tweets))):
        tweet = bearish_tweets[i]
        bearish_tweets_display.append({'text': tweet.get_truncated_text(),
                                       'link': tweet.get_link()})


    # Get 5 most recent financial news about the symbol to display
    financial_news = list(get_financial_news(symbol, n_display))
    news_article_display = []
    for i in range(min(n_display, len(financial_news))):
        article = financial_news[i]
        news_article_display.append({'title': article.get_truncated_title(),
                                     'link': article.url})
    

    return render_template('analysis.html', symbol=symbol, company_name=company_name, prediction=price_movement_prediction,
    confidence_level=confidence_level, bullish_tweets=bullish_tweets_display, bearish_tweets=bearish_tweets_display,
    news=news_article_display)
