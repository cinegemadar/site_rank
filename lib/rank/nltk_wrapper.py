from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer


class NltkWrapper():
    """Facade class for the NLTK package"""

    def __init__(self, lang='english', length_limit=2):
        """Initilaize NltkWrapper, default language is English"""

        self.limit = length_limit
        self.stopwords = stopwords.words(lang)
        self.stemmer = PorterStemmer()

    def remove_stopword(self, word_list):
        """Remove stopwords from list of words"""

        return [word for word in word_list if word not in self.stopwords]

    def tokenize(self, text):
        """Tokenize string"""

        return word_tokenize(text)

    def stem(self, words):
        """Return stemmed word list, filter out words below a given length."""

        return [str(self.stemmer.stem(word)).lower() for word in words
                if len(word) > self.limit]

    def get_sanitized_word_list(self, text):
        """Return tokenized, stemmed list of words containing no stop words."""

        no_stopword_list = self.remove_stopword(self.tokenize(text))
        return self.stem(no_stopword_list)


"""
TEST
"""


class TestNltkWrapper():
    """NLTK wrapper test class"""

    def __init__(self):
        """Init test class"""

        self.sample = '''
         Anyone who reads Old and Middle English literary texts
         will be familiar with the mid-brown volumes of the EETS, with
         the symbol of Alfred's jewel embossed on the front cover. Most
         of the works attributed to  King Alfred or to Aelfric, along
         with some of those by bishop Wulfstan and much anonymous prose
         and verse from the pre-Conquest period, are to be found within
         the Society's three series; all of the surviving medieval drama,
         most of the Middle English romances, much religious and
         secular prose and verse including the English works of John
         Gower, Thomas Hoccleve and most of Caxton's prints all find their
         place in the publications. Without EETS editions, study of medieval
         English texts would hardly be possible.
        '''
        self.processor = NltkWrapper('english')

    def test(self):
        """Run test"""

        print(self.processor.get_sanitized_word_list(self.sample))
