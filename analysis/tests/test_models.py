import unittest
from api.tweet import Tweet
from ..models import predict_price_movement, get_top_tweets, clean_text


class TestModels(unittest.TestCase):

    def setUp(self):
        tweet_one = Tweet(id='', date='', symbol='', text='$MSFT $AAPL $AMZN big three', likes=0)
        tweet_two = Tweet(id='', date='', symbol='', text='$AMD good action', likes=0)
        tweet_three = Tweet(id='', date='', symbol='', text='$MSFT $MSFT is good', likes=0)
        self.test_tweets = [tweet_one, tweet_two, tweet_three]


    def clean_text_removes_link_lowercase_words_and_lemmatizes(self):
        test_text = '$MSFT going up in price action https://twitter.com/user/status/1402982617490903040'
        actual_text = clean_text(test_text)
        expected_text = "$ msft go up in price action"
        self.assertEqual(actual_text, expected_text)


    def test_predict_price_movement_prediction_is_binary_value_of_0_or_1(self):
        prediction, _ = predict_price_movement(self.test_tweets) 
        expected_values = [0, 1]
        self.assertIn(prediction, expected_values)


    def test_predict_price_movement_confidence_level_between_0_and_100(self):
        _, confidence_level = predict_price_movement(self.test_tweets)
        self.assertGreaterEqual(confidence_level, 0)
        self.assertLessEqual(confidence_level, 100)

    
    def test_get_top_tweets_returns_tuple(self):
        top_tweets = get_top_tweets(self.test_tweets)
        self.assertIsInstance(top_tweets, tuple)


    def test_get_top_tweets_tuple_element_are_list_of_tweet_objects(self):
        bullish_tweets, bearish_tweets = get_top_tweets(self.test_tweets)
        for item in bullish_tweets:
            self.assertIsInstance(item, Tweet)

        for item in bearish_tweets:
            self.assertIsInstance(item, Tweet)
