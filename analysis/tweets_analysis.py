from api.twitter_api import get_financial_tweets
from .preprocessing import remove_bot_tweets, remove_multiple_symbol_tweets
from .models import predict_price_movement, get_top_tweets


# Labels used by machine learning models
BEARISH = 0
BULLISH = 1

def analyse_symbol(symbol):
    """Get the financial analysis for given symbol.

    Perform financial analysis on given symbol by analysing the tweets
    around the symbol. Queries tweets about the given symbol and uses
    machine learning models to predict the price movement direction.

    Args:
        symbol (str): Stock symbol to analyse

    Returns: 
        dict: Dictionary with the following keys:
            'is_bullish': boolean stating whether the model predicts
                whether the sentiment of the stock is bullish
            'confidence_level': confidence level for prediction
            'bullish_tweets': list of top bullish Tweet objects predicted by model
            'bearish_tweets': list of top bearish Tweet objects predicted by model
 
    """
    # Get up to 30 financial tweets on given symbol
    tweets = get_financial_tweets(symbol=symbol, result_type='mixed', n_items=30, date_range="today")

    # Perform cleaning to fit into machine learning models
    filtered_tweets = remove_bot_tweets(tweets)
    filtered_tweets = remove_multiple_symbol_tweets(filtered_tweets)

    prediction, confidence_level = predict_price_movement(filtered_tweets)
    bullish_tweets, bearish_tweets= get_top_tweets(filtered_tweets)
    is_bullish = prediction == BULLISH

    return {
        'is_bullish': is_bullish,
        'confidence_level': confidence_level,
        'bullish_tweets': bullish_tweets,
        'bearish_tweets': bearish_tweets
    }
