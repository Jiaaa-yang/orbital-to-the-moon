class Tweet():
    """Represents a single financial tweet.

    A class to represent a Tweet object which encapsulates
    all information of a financial tweet. It also provides methods
    to get additional information on a tweet, including the link
    to the original tweet and the truncated text version of it.

    Attributes:
        id (str): ID of current tweet
        date (str): Date where tweet was posted at, in YYYY-MM-DD format
        symbol (str): Symbol of stock the tweet is associated with
        text (str): Text content of the tweet
        likes (int): Number of likes of current tweet

    """
    def __init__(self, id, date, symbol, text, likes):
        """Constructor for a new tweet object

        Creates a new Tweet object with 'id', 'date', 'symbol' and
        'text' attributes. All the attributes must be present. 

        Args:
            id (str): ID of current tweet
            date (str): Date where tweet was posted at, in YYYY-MM-DD format
            symbol (str): Symbol of stock the tweet is associated with
            text (str): Text content of the tweet
            likes (int): Number of likes of current tweet

        """
        self.id = id
        self.date = date
        self.symbol = symbol
        self.text = text
        self.likes = likes

    
    def get_link(self):
        """Get the link to the tweet referred by current object

        Returns the Twitter link to the original tweet that the current 
        Tweet is referring to, by referencing the id of the Tweet.

        Returns:
            Twitter link of current Tweet

        Raises:
            ValueError: If ID field is empty
        
        """
        if self.id == "":
            raise ValueError("ID field for Tweet is empty")

        return f"https://twitter.com/user/status/{self.id}"

    
    def get_truncated_text(self, word_len=12, ending="..."):
        """Get the truncated text of current tweet.

        Returns the truncated text of current Tweet up to given
        word_len number of words, appended by given ending string.
        If the length of the text is lesser than word_len, returns
        the original text.

        Args:
            word_len (int, optional): Number of words to truncate text
                to, defaults to 12
            ending (str, optional): Ending string to append to truncated
                text, defaults to ellipsis, '...'

        Returns:
            Truncated text of the text content of current tweet

        """
        words_in_text = self.text.split()
        if len(words_in_text) <= word_len:
            return self.text

        # Take the first word_len words from list of words split from text
        # and append given ending to text
        truncated_text = " ".join(words_in_text[:word_len])
        return truncated_text + ending
