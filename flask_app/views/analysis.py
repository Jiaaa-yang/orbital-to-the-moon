from concurrent.futures import ThreadPoolExecutor
from analysis.tweets_analysis import analyse_symbol
from api.mediastack_api import get_financial_news
from flask import (
    Blueprint, redirect, render_template, flash, request, session
)
import yfinance as yf


bp = Blueprint('analysis', __name__)

@bp.route('/analysis/<symbol>')
def analysis(symbol):
    # Get up to 5 items to display for each section and pass them
    # as a list of dictionary with relevant data
    n_display = 5
    bullish_tweets_display = []
    bearish_tweets_display = []
    news_article_display = []

    # Whether current symbol is favourited by user in session information
    is_favourite = symbol in session['favourites']

    # Use multithreading for the API calls required
    with ThreadPoolExecutor(max_workers=5) as executor:
        get_stock_info = lambda symbol: yf.Ticker(symbol).info
        stock_info_future = executor.submit(get_stock_info, symbol)
        analysis_future = executor.submit(analyse_symbol, symbol)
        financial_news_future = executor.submit(get_financial_news, symbol, n_display)

        stock_info = stock_info_future.result()
        if len(stock_info) == 1:
            # Stock does not exist from lookup on Yahoo Finance
            flash('No matching company listing found')
            return redirect('/')

        analysis = analysis_future.result()
        company_name = stock_info['shortName']
        price_movement_prediction = "RISE" if analysis['is_bullish'] else "FALL"
        confidence_level = "{:.2f}".format(analysis['confidence_level'])
        bullish_tweets = analysis['bullish_tweets']
        bearish_tweets = analysis['bearish_tweets']

        # Add dictionaries to each list of display tweets, each containing
        # a 'text' and 'link' key
        for i in range(min(n_display, len(bullish_tweets))):
            tweet = bullish_tweets[i]
            bullish_tweets_display.append({'text': tweet.get_truncated_text(),
                                        'link': tweet.get_link()})

        for i in range(min(n_display, len(bearish_tweets))):
            tweet = bearish_tweets[i]
            bearish_tweets_display.append({'text': tweet.get_truncated_text(),
                                        'link': tweet.get_link()})


        # Get 5 most recent financial news about the symbol to display
        financial_news = financial_news_future.result()
        for i in range(min(n_display, len(financial_news))):
            article = financial_news[i]
            news_article_display.append({'title': article.get_truncated_title(),
                                        'link': article.url})
        

        return render_template('analysis.html', is_favourite=is_favourite, symbol=symbol, company_name=company_name, 
        prediction=price_movement_prediction, confidence_level=confidence_level, bullish_tweets=bullish_tweets_display, 
        bearish_tweets=bearish_tweets_display, news=news_article_display)


@bp.route('/add-favourites', methods=['GET', "POST"])
def add_favourite():
    if request.method == 'POST':
        # Add favourited stock to session info if it does not already exist
        # and create a new list if session info is empty 
        symbol = request.form.to_dict()['symbol']
        if session.get('favourites'):
            if symbol not in session['favourites']:
                session['favourites'] = session['favourites'] + [symbol]
        else:
            session['favourites'] = [symbol]

        return analysis(symbol)
