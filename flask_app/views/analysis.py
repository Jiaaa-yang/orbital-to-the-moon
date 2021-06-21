from analysis.tweets_analysis import analyse_symbol
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

    # Get up to 3 most bullish tweets to display and truncate their text
    # to 12 words long, and construct their link from id
    num_display_tweets = 3
    text_len = 12
    display_tweets = []

    for i in range(min(num_display_tweets, len(bullish_tweets))):
        tweet = bullish_tweets[i]
        text = tweet['tweet'].split()
        truncated_text = " ".join(text[:min(len(text), text_len)]) + "..."
        tweet_link = f"https://twitter.com/user/status/{tweet['id']}"
        display_tweets.append({'text': truncated_text, 'link': tweet_link})

    return render_template('analysis.html', symbol=symbol, company_name=company_name, prediction=price_movement_prediction,
    confidence_level=confidence_level, display_tweets=display_tweets)
