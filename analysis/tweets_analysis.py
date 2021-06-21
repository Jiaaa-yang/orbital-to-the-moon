from api.twitter_api import get_financial_tweets
from .preprocessing import (
    remove_bot_tweets, remove_multiple_symbol_tweets, clean_tweets_list
)
from .models import predict_price_movement, get_top_tweets

def analyse_symbol(symbol):
    """Get the financial analysis for given symbol.

    Perform financial analysis on given symbol by analysing the tweets
    around the symbol. Queries tweets about the given symbol and uses
    machine learning models to predict the price movement direction.

    Args:
        symbol (str): Stock symbol to analyse

    Returns: 
        dict: Dictionary with the following keys:
            'price_rise': boolean stating whether the model predicts
                the price for given stock to rise
            'confidence_level': confidence level for prediction
            'bullish_tweets': list of top bullish tweets in dictionary form with 'id', 'date',
                'symbol' and 'tweet' keys 
            'bearish_tweets': list of top bearish tweets in dictionary form with 'id', 'date',
                'symbol' and 'tweet' keys
 
    """
    # Get up to 30 financial tweets on given symbol
    tweets = get_financial_tweets(symbol=symbol, result_type='mixed', n_items=30)

    # Perform cleaning to fit into machine learning models
    filtered_tweets = remove_bot_tweets(tweets)
    filtered_tweets = remove_multiple_symbol_tweets(filtered_tweets)
    cleaned_tweets = clean_tweets_list(filtered_tweets)

    prediction, confidence_level = predict_price_movement(cleaned_tweets)
    bullish_tweets_index, bearish_tweets_index = get_top_tweets(cleaned_tweets)

    price_rise = prediction == 1
    bullish_tweets = [filtered_tweets[index] for index in bullish_tweets_index]
    bearish_tweets = [filtered_tweets[index] for index in bearish_tweets_index]

    return {
        'price_rise': price_rise,
        'confidence_level': confidence_level,
        'bullish_tweets': bullish_tweets,
        'bearish_tweets': bearish_tweets
    }
