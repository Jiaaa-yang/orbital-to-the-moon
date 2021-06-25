import unittest
from ..tweet import Tweet


class TestTweet(unittest.TestCase):

    def test_get_link_works_with_valid_id(self):
        test_tweet = Tweet(id='1234', date='200-01-01', symbol='MSFT', text='test string')
        expected_link = "https://twitter.com/user/status/1234" 
        actual_link = test_tweet.get_link()
        self.assertEqual(actual_link, expected_link)


    def test_get_link_raises_value_error_with_empty_id(self):
        test_tweet = Tweet(id='', date='200-01-01', symbol='MSFT', text='test string')
        self.assertRaises(ValueError, test_tweet.get_link)


    def test_get_truncated_text_truncates_long_text(self):
        long_text = "this is a long text with a word length greater than 12 words in total"
        test_tweet = Tweet(id='', date='200-01-01', symbol='MSFT', text=long_text)
        actual_text = test_tweet.get_truncated_text()
        expected_text = "this is a long text with a word length greater than 12..."
        self.assertEqual(actual_text, expected_text)


    def test_get_truncated_text_leaves_short_text_unchanged(self):
        short_text = "this is a short text"
        test_tweet = Tweet(id='', date='2000-01-01', symbol='MSFT', text=short_text)
        actual_text = test_tweet.get_truncated_text()
        self.assertEqual(actual_text, short_text)


    def test_get_truncated_text_works_with_non_default_arguments(self):
        test_tweet = Tweet(id='1234', date='200-01-01', symbol='MSFT', text='text with 4 words')
        actual_text = test_tweet.get_truncated_text(word_len=2, ending='!!!')
        expected_test = 'text with!!!'
        self.assertEqual(actual_text, expected_test)
