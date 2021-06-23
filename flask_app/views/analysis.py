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
    price_movement_prediction = "RISE" if analysis['price_rise'] else "FALL"
    confidence_level = "{:.2f}".format(analysis['confidence_level'])
    bullish_tweets = analysis['bullish_tweets']
    bearish_tweets = analysis['bearish_tweets']

    # Get up to 3 most bullish tweets to display and truncate their text
    # to 12 words long, and construct their link from id
    num_display_tweets = 3
    text_len = 12
    bullish_tweets_display = []
    bearish_tweets_display = []

    for i in range(min(num_display_tweets, len(bullish_tweets))):
        tweet = bullish_tweets[i]
        text = tweet['tweet'].split()
        truncated_text = " ".join(text[:min(len(text), text_len)]) + "..."
        tweet_link = f"https://twitter.com/user/status/{tweet['id']}"
        bullish_tweets_display.append({'text': truncated_text, 'link': tweet_link})

    for i in range(min(num_display_tweets, len(bearish_tweets))):
        tweet = bearish_tweets[i]
        text = tweet['tweet'].split()
        truncated_text = " ".join(text[:min(len(text), text_len)]) + "..."
        tweet_link = f"https://twitter.com/user/status/{tweet['id']}"
        bearish_tweets_display.append({'text': truncated_text, 'link': tweet_link})

    # Get 5 most recent financial news about the symbol to display
    num_display_news = 5
    news_display = []
    financial_news = list(get_financial_news(symbol, num_display_news))
    for i in range(min(num_display_news, len(financial_news))):
        title = financial_news[i]['title'].split()
        truncated_title = " ".join(title[:min(len(title), text_len)]) + "..."
        link = financial_news[i]['url']
        news_display.append({'title': truncated_title, 'link': link})
    

    return render_template('analysis.html', symbol=symbol, company_name=company_name, prediction=price_movement_prediction,
    confidence_level=confidence_level, bullish_tweets=bullish_tweets_display, bearish_tweets=bearish_tweets_display,
    news=news_display)
