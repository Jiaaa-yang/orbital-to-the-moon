import unittest
from ..article import Article


class TestArticle(unittest.TestCase):

    def test_get_truncated_title_truncates_long_title(self):
        long_title = "this is a long title with a word length greater than 12 words in total"
        test_article = Article(title=long_title, description='test', date='2020-01-01', symbol='MSFT', url='test')
        actual_text = test_article.get_truncated_title()
        expected_text = "this is a long title with a word length greater than 12..."
        self.assertEqual(actual_text, expected_text)


    def test_get_truncated_title_leaves_short_title_unchanged(self):
        short_title = "this is a short title"
        test_article = Article(title=short_title, description='test', date='2020-01-01', symbol='MSFT', url='test')
        actual_text = test_article.get_truncated_title()
        self.assertEqual(actual_text, short_title)


    def test_get_truncated_title_works_with_non_default_arguments(self):
        test_article = Article(title='text with 4 words', description='test', date='2020-01-01', symbol='MSFT', url='test')
        actual_text = test_article.get_truncated_title(word_len=2, ending='!!!')
        expected_test = 'text with!!!'
        self.assertEqual(actual_text, expected_test)
