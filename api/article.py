class Article():
    """Represents a single financial news article.

    A class to represent a Article object which encapsulates
    all information of a financial news article. It also provides a 
    method to get the truncated version of its title for display.

    Attributes:
        title (str): Title of current article
        description (str): Description of current article
        date (str): Date the article was published at
        symbol (str): Stock symbol associated with current article
        url (str): Url to the original news article

    """
    def __init__(self, title, description, date, symbol, url):
        """Constructor for a new article object

        Creates a new Tweet object with 'title', 'description', 'date',
        'symbol' and 'url' attributes. All the attributes must be present. 

        Args:
            title (str): Title of article to create
            description (str): Description of article to create
            date (str): Date the article was published at
            symbol (str): Stock symbol associated with article to create
            url (str): Url to the original news article

        """
        self.title = title
        self.description = description
        self.date = date
        self.symbol = symbol
        self.url = url

    
    def get_truncated_title(self, word_len=12, ending="..."):
        """Get the truncated title of current article.

        Returns the truncated article of current Article up to given
        word_len number of words, appended by given ending string.
        If the length of the text is lesser than word_len, returns
        the original text.

        Args:
            word_len (int, optional): Number of words to truncate text
                to, defaults to 12
            ending (str, optional): Ending string to append to truncated
                text, defaults to ellipsis, '...'

        Returns:
            Truncated title of current article

        """
        words_in_title = self.title.split()
        if len(words_in_title) <= word_len:
            return self.title

        # Take the first word_len words from list of words split from text
        # and append given ending to text
        truncated_text = " ".join(words_in_title[:word_len])
        return truncated_text + ending
