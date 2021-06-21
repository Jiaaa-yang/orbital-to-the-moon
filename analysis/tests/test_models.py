import unittest
from ..models import predict_price_movement, get_top_tweets

class TestPreprocessing(unittest.TestCase):

    def setUp(self):
        tweet_one = {'id': 0, 'date': '2000-01-01', 'symbol': 'AMD', 'tweet': '$MSFT $AAPL $AMZN big three'}
        tweet_two = {'id': 0, 'date': '2000-01-01', 'symbol': 'AMD', 'tweet': '$AMD good action'}
        tweet_three = {'id': 0, 'date': '2000-01-01', 'symbol': 'AMD', 'tweet': '$MSFT $MSFT is good'}
        self.test_tweets = [tweet_one, tweet_two, tweet_three]


    def test_predict_price_movement_prediction_is_binary(self):
        prediction, _ = predict_price_movement(self.test_tweets) 
        expected_values = [0, 1]
        self.assertIn(prediction, expected_values)


    def test_predict_price_movement_confidence_level_between_0_and_100(self):
        _, confidence_level = predict_price_movement(self.test_tweets)
        self.assertGreaterEqual(confidence_level, 0)
        self.assertLessEqual(confidence_level, 100)

    
    def test_get_top_tweets_returns_valid_index(self):
        bullish_tweets, bearish_tweets = get_top_tweets(self.test_tweets)
        valid_indexes = range(len(self.test_tweets))
        for index in bullish_tweets:
            self.assertIn(index, valid_indexes)

        for index in bearish_tweets:
            self.assertIn(index, valid_indexes)