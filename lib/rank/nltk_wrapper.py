from nltk.corpus import stopwords
from nltk import word_tokenize

class NltkWrapper():


    def __init__(self, lang='english'):
        self.stopwords = stopwords.words(lang)

    def remove_stopword(self, word_list):
        return [word for word in word_list if word not in self.stopwords]

    def tokenize(self, text):
        return word_tokenize(text)

    def get_sanitized_word_list(self, text, limit=3):
        return [word for word in self.remove_stopword(self.tokenize(text)) if len(word) > limit ]

"""
TEST


sample = '''Anyone who reads Old and Middle English literary texts 
will be familiar with the mid-brown volumes of the EETS, with the symbol 
of Alfred's jewel embossed on the front cover. Most of the works attributed to 
King Alfred or to Aelfric, along with some of those by bishop Wulfstan and much 
anonymous prose and verse from the pre-Conquest period, are to be found within the 
Society's three series; all of the surviving medieval drama, most of the Middle English 
romances, much religious and secular prose and verse including the English works of John 
Gower, Thomas Hoccleve and most of Caxton's prints all find their place in the publications.
Without EETS editions, study of medieval English texts would hardly be possible.'''

processor = NltkWrapper('english')

print(processor.get_sanitized_word_list(sample))

"""