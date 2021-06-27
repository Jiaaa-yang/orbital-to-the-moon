from joblib import load
import re
from analysis import nlp


# Labels used by machine learning models
BEARISH = 0
BULLISH = 1

vectorizer = load("analysis/sklearn_saved_models/vectorizer.joblib")
text_labeller = load("analysis/sklearn_saved_models/svm_classifier.joblib")
price_predictor = load("analysis/sklearn_saved_models/rand_forest_classifier.joblib")

def clean_text(text):
    """Clean given text

    Cleans given text in same form as text was cleaned before
    feeding into machine learning models. Removes links, 
    tweet account handles, '&amp;'. Also lowercases all words
    and change all words into their lemma form. 

    Args:
        text (str): Text content of tweet to clean

    Returns: 
        str: Cleaned text

    """
    text = re.sub('(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)', '', text) # Remove links
    text = re.sub('@(\w+)', '', text) # Remove account handles
    text = re.sub('&amp;', '', text) # Remove ampersand from text
    text = text.lower()
    doc = nlp(text)
    text = " ".join([token.lemma_ for token in doc])
    return " ".join(text.split())


def predict_price_movement(tweets_list):
    """Predict whether price of stock will rise from given tweets.

    Using trained machine learning models, pass the text content of the tweets
    through the models to predict whether the prices will go up or down and
    the confidence level.

    Args:
        tweets_list (iterator): List of Tweet objects

    Returns: 
        tuple: Tuple of two elements, the first is a integer of either '0' representing
            a prediction of bearish sentiment, and a '1' for bullish sentiment. The second element
            is a float between 0 and 100 which represents the probability/confidence level
            of the prediction

    """
    # Return default values if there are no available tweets
    if len(tweets_list) == 0:
        return 0, 0

    # Convert list of tweets into vector of cleaned text content to
    # be transformed by vectorizer
    corpus = [tweet.text for tweet in tweets_list]
    corpus = list(map(clean_text, corpus))
    tfidf_matrix = vectorizer.transform(corpus)

    # Use the trained labeller to find how many tweets have bullish sentiment
    total_tweets = len(corpus)
    bullish_tweets = 0
    for vector in tfidf_matrix:
        label = text_labeller.predict(vector)[0]
        if label == BULLISH:
            bullish_tweets += 1

    # Use number of bullish and total tweets to predict price movement direction
    feature = [[bullish_tweets, total_tweets]]
    prediction = int(price_predictor.predict(feature)[0])
    confidence_level = float(max(price_predictor.predict_proba(feature)[0]) * 100)

    return prediction, confidence_level


def get_top_tweets(tweets_list):
    """Get list of top bullish and bearish tweets from given tweets list.

    Get the two lists of tweets from given tweets that have the highest confidence level
    of being bullish and bearish. The returned list for each bullish and bearish tweets
    are sorted such that the first element contains the tweet with the highest confidence
    score to be bullish/bearish respectively.

    Args:
        tweets_list (iterator): List of Tweet objects

    Returns: 
        tuple: Tuple with 2 elements, the first is a list of bullish tweets sorted with 
            the most bullish tweet being the first element, and the second is the 
            sorted list of bearish tweets

    """
    # Return default values if there are no available tweets
    if len(tweets_list) == 0:
        return [], []

    corpus = [tweet.text for tweet in tweets_list]
    corpus = list(map(clean_text, corpus))
    tfidf_matrix = vectorizer.transform(corpus)
    
    bullish_tweets = []
    bearish_tweets = []
    for i, vector in enumerate(tfidf_matrix):
        # For each text corresponding to the Tweet at index i
        # of the given list, append the tweet and the confidence score
        # of the prediction to the list of bullish/bearish tweets
        label = text_labeller.predict(vector)[0]
        confidence_score = abs(text_labeller.decision_function(vector)[0])
        if label == BULLISH:
            bullish_tweets.append((tweets_list[i], confidence_score))
        elif label == BEARISH:
            bearish_tweets.append((tweets_list[i], confidence_score))
    

    # Sort the tweets by confidence score such that the most bullish/bearish tweets 
    # with the highest confidence score are first in the list
    bullish_tweets = [tweet for tweet, _ in sorted(bullish_tweets, key=lambda pair: pair[1], reverse=True)]
    bearish_tweets = [tweet for tweet, _ in sorted(bearish_tweets, key=lambda pair: pair[1], reverse=True)]
    return bullish_tweets, bearish_tweets
