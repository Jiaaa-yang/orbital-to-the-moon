import unittest
from api.tweet import Tweet
from ..preprocessing import (
    remove_bot_tweets, remove_multiple_symbol_tweets
)

class TestPreprocessing(unittest.TestCase):

    def test_remove_bot_tweets_remove_text_containing_bot_phrases(self):
        normal_tweet_one = Tweet(id='', date='', symbol='', text='normal tweet one', likes=0)
        bot_tweet_one = Tweet(id='', date='', symbol='', text='sec alert new trade', likes=0)
        normal_tweet_two = Tweet(id='', date='', symbol='', text='normal tweet two', likes=0)
        bot_tweet_two = Tweet(id='', date='', symbol='', text='for real time prints check out', likes=0)
        actual_filtered_tweets = remove_bot_tweets([normal_tweet_one, bot_tweet_one, normal_tweet_two, bot_tweet_two]) 
        expected_tweets = [normal_tweet_one, normal_tweet_two]
        # Check filtered tweets have same content as expected, regardless of order
        self.assertCountEqual(actual_filtered_tweets, expected_tweets)


    def test_remove_multiple_symbol_tweets_remove_text_containing_multiple_symbols(self):
        tweet_one = Tweet(id='', date='', symbol='', text='$MSFT $AAPL $AMZN big three', likes=0)
        tweet_two = Tweet(id='', date='', symbol='', text='$AMD good action', likes=0)
        tweet_three = Tweet(id='', date='', symbol='', text='$MSFT $MSFT seeing good volume', likes=0)
        actual_filtered_tweets = remove_multiple_symbol_tweets([tweet_one, tweet_two, tweet_three]) 
        expected_tweets = [tweet_two, tweet_three]
        # Check filtered tweets have same content as expected, regardless of order
        self.assertCountEqual(actual_filtered_tweets, expected_tweets)
