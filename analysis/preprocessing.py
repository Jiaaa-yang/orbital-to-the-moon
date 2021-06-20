import spacy
import re


# Load text processing model from spacy and add symbol matcher
nlp = spacy.load('en_core_web_lg')

matcher = spacy.matcher.Matcher(nlp.vocab)
symbol_pattern = [{"TEXT":"$"}, {"POS": {"IN": ["NOUN", "PROPN", "VERB", "ADJ"]}}]
matcher.add("symbols", [symbol_pattern])

def remove_bot_tweets(tweets_list):
    """Remove tweets by bots from given tweets.

    Filter out tweets by bot accounts from given list of
    tweets by checking whether they contain any of the pre-determined
    bot phrases.

    Args:
        tweets_list (iterator): Iterable of tweets in a dictionary form,
            with given keys: 'id', 'date', 'symbol', 'tweet'

    Returns: 
        list: List of tweets in dictionary form with bot tweets filtered out,
            and with the given keys: 'id', 'date', 'symbol', 'tweet'

    """
    # Phrases associated with tweets by bot accounts
    bot_phrases = ['for real time prints', 'sec alert', '1 minute', '#options', 'companies in our database',
                'by the same day\'s market close', 'technical alerts', 'new alert', 'chatroom', 'trade alert',
                'if you know trading around print', 'view odds for this', '15s. delayed', 'tradewithalerts']

    # Lambda function to check if given text is likely to be a bot tweet
    # by checking if it contains any of the bot phrases
    is_bot_tweet = lambda text: any([bot_phrase in text for bot_phrase in bot_phrases])
    filtered_tweets = []
    for tweet in tweets_list:
        text = tweet['tweet'].lower()
        if not is_bot_tweet(text):
            filtered_tweets.append(tweet)

    return filtered_tweets


def num_symbols_mentioned(text):
    """Get number of symbols mentioned in given text.

    Using spaCy's rule-based matcher, get the number of symbols
    mentioned in given text. This is a probability model and may not find
    all symbols mentioned in the text.

    Args:
        text (str): Text content of tweet

    Returns: 
        int: Number of symbols mentioned in the text

    """
    doc = nlp(text)
    symbols_found = set()
    for _, start, end in matcher(doc):
        symbol = doc[start:end].text
        symbols_found.add(symbol.lower())
    return len(symbols_found)


def remove_multiple_symbol_tweets(tweets_list):
    """Remove tweets on multiple symbols.

    Filter out financial tweets which mention multiple symbols
    by using spaCy's rule-based matcher. May not be completely accurate
    as this uses a probability model.

    Args:
        tweets_list (iterator): Iterable of tweets in a dictionary form,
            with given keys: 'id', 'date', 'symbol', 'tweet'

    Returns: 
        list: List of tweets in dictionary form with multiple symbol tweets 
            filtered out, and with the given keys: 'id', 'date', 'symbol', 'tweet'

    """
    filtered_tweets = []
    for tweet in tweets_list:
        text = tweet['tweet']
        if num_symbols_mentioned(text) <= 1:
            filtered_tweets.append(tweet)

    return filtered_tweets


def clean_text(text):
    """Clean given text

    Remove links, tweet account handles, '&amp;'. Also lowercases all words
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


def clean_tweets_list(tweets_list):
    """Clean text content of all tweets

    Perform cleaning on the tweet in the same way as was done to the
    training tweets before feeding into machine learning models. Remove links,
    tweet account handles, '&amp;', lowercases and lemmatizes words.

    Args:
        tweets_list (iterator): Iterable of tweets in a dictionary form,
            with given keys: 'id', 'date', 'symbol', 'tweet'

    Returns: 
        list: List of tweets in dictionary form with tweet text content cleaned,
            and with the given keys: 'id', 'date', 'symbol', 'tweet'

    """
    filtered_tweets = []
    for tweet in tweets_list:
        tweet['tweet'] = clean_text(tweet['tweet'])
        filtered_tweets.append(tweet)

    return filtered_tweets
