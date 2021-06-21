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


def get_top_tweets(tweets_list):
    """Get list of top bullish and bearish tweets from given tweets list.

    Get the indexes of subset from given tweets that have the highest confidence level
    of being bullish and bearish. The returned list for each bullish and bearish tweets
    are sorted such that the first element contains the tweet with the highest confidence
    score to be bullish/bearish respectively.

    Args:
        tweets_list (iterator): Iterable of tweets in a dictionary form,
            with given keys: 'id', 'date', 'symbol', 'tweet'

    Returns: 
        tuple: Tuple with 2 elements, the first is the indexes of bullish tweets sorted with 
            the most bullish tweet being the first element, and the second is the indexes of
            the sorted list of bearish tweets

    """
    text = [tweet['tweet'] for tweet in tweets_list]
    tfidf_matrix = vectorizer.transform(text)
    
    bullish_tweets_indexes = []
    bearish_tweets_indexes = []
    for index, vector in enumerate(tfidf_matrix):
        label = text_labeller.predict(vector)[0]
        confidence_score = abs(text_labeller.decision_function(vector)[0])
        if label == BULLISH:
            bullish_tweets_indexes.append((index, confidence_score))
        elif label == BEARISH:
            bearish_tweets_indexes.append((index, confidence_score))
    
    bullish_tweets = [index for index, _ in sorted(bullish_tweets_indexes, key=lambda pair: pair[1])]
    bearish_tweets = [index for index, _ in sorted(bearish_tweets_indexes, key=lambda pair: pair[1])]
    return bullish_tweets, bearish_tweets
