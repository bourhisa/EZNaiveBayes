import nltk
nltk.data.path.append("/media/arnaud/Data/workspace/nltk_data");
nltk.data.path.append("D:/workspace/nltk_data");
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from stop_words import get_stop_words
import itertools
from config import *


class Item():
    label = '' # "positive" or "negative"
    tokens = [] # List of all the tokens
    text = ''

    def __init__(self, rawitem):
        self.tokens = []
        self.label = rawitem['label']
        try:
            self.text = rawitem['text'].decode('utf-8')
            self.build_tokens()
        except:
            pass

    def build_tokens(self):  # Takes care of the stemming, stopwords and tokenization

        if DELETE_STOPWORDS:
            tokens = [word for word in nltk.word_tokenize(self.text) if word not in stopwords.words('english')]
        else:
            tokens = [word for word in nltk.word_tokenize(self.text)]

        if STEMMING:
            stemmer = SnowballStemmer("english", ignore_stopwords = True)
            self.stem(stemmer)

        # Grouping monograms and bigrams
        n_grams = []
        dict_features = {}

        for t in tokens:  # Monograms
            n_grams.append(t)

        if TWO_CONSECUTIVE:  # (N, N+1)
            n_grams += (['+'.join(sorted([tokens[t], tokens[t + 1]])) for t in range(len(tokens) - 1)])


        if TWO_AHEAD: # (N, N+2)
            n_grams += (['+'.join(sorted([tokens[t], tokens[t + 2]])) for t in range(len(tokens) - 2)])

        if THREE_CONSECUTIVE:  # (N, N+1, N+2)
            n_grams += (['+'.join(sorted([tokens[t], tokens[t + 1], tokens[t+2]])) for t in range(len(tokens) - 2)])

        if TWO_RANDOM:  # All combinations of 2 words within a phrase
            for t in itertools.combinations(tokens, 2):
                n_grams.append('+'.join(sorted(t)))

        self.tokens = n_grams


    def stem(self, stemmer):
        stemmed = []
        for t in self.tokens:
            stemmed.append(stemmer.stem(t))
        self.tokens = stemmed

    def __del__(self):
        self.label = ''
        self.tokens = []
        self.text = ''