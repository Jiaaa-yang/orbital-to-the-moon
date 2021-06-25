import spacy
from analysis import nlp


# Add symbol matcher to find mention of ticker symbols
matcher = spacy.matcher.Matcher(nlp.vocab)
symbol_pattern = [{"TEXT":"$"}, {"POS": {"IN": ["NOUN", "PROPN", "VERB", "ADJ"]}}]
matcher.add("symbols", [symbol_pattern])

def remove_bot_tweets(tweets_list):
    """Remove tweets by bots from given tweets.

    Filter out tweets by bot accounts from given list of
    tweets by checking whether they contain any of the pre-determined
    bot phrases.

    Args:
        tweets_list (iterator): List of Tweet objects

    Returns: 
        list: List of Tweet objects with bot tweets filtered out

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
        text = tweet.text.lower()
        if not is_bot_tweet(text):
            filtered_tweets.append(tweet)

    return filtered_tweets


def _num_symbols_mentioned(text):
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
        tweets_list (iterator): Iterable of Tweet objects

    Returns: 
        list: List of Tweet object with multiple symbol tweets filtered out

    """
    filtered_tweets = []
    for tweet in tweets_list:
        text = tweet.text
        if _num_symbols_mentioned(text) <= 1:
            filtered_tweets.append(tweet)

    return filtered_tweets
