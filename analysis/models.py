from joblib import load


# Labels used by machine learning models
BEARISH = 0
BULLISH = 1

vectorizer = load("analysis/sklearn_saved_models/vectorizer.joblib")
text_labeller = load("analysis/sklearn_saved_models/svm_classifier.joblib")
price_predictor = load("analysis/sklearn_saved_models/rand_forest_classifier.joblib")

def predict_price_movement(tweets_list):
    """Predict whether price of stock will rise from given tweets.

    Using trained machine learning models, pass the text content of the tweets
    through the models to predict whether the prices will go up or down and
    the confidence level.

    Args:
        tweets_list (iterator): Iterable of tweets in a dictionary form,
            with given keys: 'id', 'date', 'symbol', 'tweet'

    Returns: 
        tuple: Tuple of two elements, the first is a integer of either '0' representing
            a prediction of falling prices, and a '1' for rising price. The second element
            is a float between 0 and 100 which represents the probability/confidence level
            of the prediction

    """
    text = [tweet['tweet'] for tweet in tweets_list]
    tfidf_matrix = vectorizer.transform(text)

    # Use the trained labeller to find how many tweets have bullish sentiment
    total_tweets = len(text)
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


def get_bullish_tweets(tweets_list):
    """Get list of bullish tweets from given tweets list.

    Get the indexes of subset from given tweets that are labelled bullish by tweet labeller.
    The tweets returned contain the confidence score for their labels, and are sorted
    such that the first element contains the tweet with the highest confidence score.

    Args:
        tweets_list (iterator): Iterable of tweets in a dictionary form,
            with given keys: 'id', 'date', 'symbol', 'tweet'

    Returns: 
        list: List of tuple containing two elements. The first is the index corresponding
            to the tweet in the original list. The second is the confidence score of the
            label of the tweet. The list returned contains the indexes of subset of the given list
            that have a bullish label, and are sorted by confidence score in descending order

    """
    text = [tweet['tweet'] for tweet in tweets_list]
    tfidf_matrix = vectorizer.transform(text)
    
    bullish_tweets_indexes = []
    for index, vector in enumerate(tfidf_matrix):
        label = text_labeller.predict(vector)[0]
        if label == BULLISH:
            confidence_score = text_labeller.decision_function(vector)[0]
            bullish_tweets_indexes.append((index, confidence_score))
    
    return sorted(bullish_tweets_indexes, key=lambda pair: pair[1])
