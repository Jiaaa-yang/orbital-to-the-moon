import unittest
from ..preprocessing import (
    remove_bot_tweets, remove_multiple_symbol_tweets, clean_tweets_list
)

class TestPreprocessing(unittest.TestCase):

    def test_bot_tweets_removed_correctly(self):
        # Test data with a few tweets containing bot phrases
        normal_tweet_one = {'id': 0, 'date': '2000-01-01', 'symbol': 'AMD', 'tweet': 'normal tweet one'}
        bot_tweet_one = {'id': 0, 'date': '2000-01-01', 'symbol': 'AMD', 'tweet': 'sec alert new trade'}
        normal_tweet_two = {'id': 0, 'date': '2000-01-01', 'symbol': 'AMD', 'tweet': 'normal tweet two'}
        bot_tweet_two = {'id': 0, 'date': '2000-01-01', 'symbol': 'AMD', 'tweet': 'for real time prints check out'}
        actual_filtered_tweets = remove_bot_tweets([normal_tweet_one, bot_tweet_one, normal_tweet_two, bot_tweet_two]) 
        expected_tweets = [normal_tweet_one, normal_tweet_two]
        # Check filtered tweets have same content as expected, regardless of order
        self.assertCountEqual(actual_filtered_tweets, expected_tweets)


    def test_multiple_symbols_tweets_removed_correctly(self):
        # Test data with a few tweets containing multiple symbols
        tweet_one = {'id': 0, 'date': '2000-01-01', 'symbol': 'AMD', 'tweet': '$MSFT $AAPL $AMZN big three'}
        tweet_two = {'id': 0, 'date': '2000-01-01', 'symbol': 'AMD', 'tweet': '$AMD good action'}
        tweet_three = {'id': 0, 'date': '2000-01-01', 'symbol': 'AMD', 'tweet': '$MSFT $MSFT is good'}
        actual_filtered_tweets = remove_multiple_symbol_tweets([tweet_one, tweet_two, tweet_three]) 
        expected_tweets = [tweet_two, tweet_three]
        # Check filtered tweets have same content as expected, regardless of order
        self.assertCountEqual(actual_filtered_tweets, expected_tweets)


    def test_text_content_cleaned(self):
        # Test data with a few tweets containing multiple symbols
        tweets = [{'id': 0, 
                   'date': '2000-01-01', 
                   'symbol': 'AMD', 
                   'tweet': '$MSFT going up in price action https://twitter.com/user/status/1402982617490903040'}]
        cleaned_tweets = clean_tweets_list(tweets) 
        actual_text = cleaned_tweets[0]['tweet']
        expected_text = "$ msft go up in price action"
        self.assertEqual(actual_text, expected_text)
