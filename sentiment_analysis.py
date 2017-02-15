#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, json, nltk, re
from collections import Counter
import itertools


IS_POSSIBLY_UNDETERMINED = True
CERTAINTY_RATE = 0.15


class Tweet():
    tokens = [] # List of all the tokens
    text = ''

    def __init__(self, rawtweet):
        self.tokens = []
        self.text = ""
        self.preprocess(rawtweet)
        self.extract_features()

    def preprocess(self, rawtweet):
        try:
            rawtweet = rawtweet.lower()
            rawtweet =  re.sub('\\n','', rawtweet) #gets rid of line breaks
            rawtweet =  re.sub('@\S*','AT_USER', rawtweet) #banalizes user references
            rawtweet =  re.sub('https?://\S*', 'URL ', rawtweet)
            rawtweet =  re.sub('www\S*', 'URL ', rawtweet) #banalizes links
            # self.text = ' \u'.join(tweet.split('\\u')) # attempt to treat emojis
            rawtweet =  re.sub("[/@'\\$`,\-#%&;.:=[{}()$0.""]", '', rawtweet) 
            self.text = rawtweet
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print(exc_type, fname, exc_tb.tb_lineno)


    def extract_features(self):

        tokens = [word for word in nltk.word_tokenize(self.text.decode('utf-8'))]

        n_grams = []
        dict_features = {}

        try:
            for t in tokens:
                n_grams.append(t)

            for t in range(len(tokens)-1): # Consecutive words
                n_grams.append('+'.join(sorted([tokens[t],tokens[t+1]]))) # Adds consecutive bigrams to n_grams


            for t in range(len(tokens)-2): # Two ahead
                n_grams.append('+'.join(sorted([tokens[t], tokens[t+2]])))

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            n_grams = []
        self.tokens = n_grams

    def __del__(self):
        self.label = ''
        self.tokens = []
        self.text = ''

class Classifier():

    global_dict = {}
    features = {}
    features_filename = ''
    classifier_filename = ''

    def __init__(self, **keyword_parameters):

        self.import_global_dict()

# Imports the previous information, or creates blank files and variables
    def import_global_dict(self):
        self.features_filename = FEATURES_FILE
        self.classifier_filename = CLASSIFIER_FILE

        # Classifier file
        if not os.path.isfile(self.classifier_filename):
            f = open(self.classifier_filename, 'w').close()
        with open(self.classifier_filename, 'r') as f:
            p = f.read()
            if f:
                try:
                    self.global_dict = Counter(json.loads(p))
                except Exception as e:
                    self.global_dict = Counter(dict())
            f.close()

        # Insights file
        if not os.path.isfile(self.features_filename):
            f = open(self.features_filename, 'w').close()
        with open(self.features_filename, 'r') as f:
            p = f.read()
            if f:
                try:
                    self.features = json.loads(p)
                except:
                    self.features = dict()
            f.close()

    def make_labels(self, tweets):
    	self.global_dict = dict(self.global_dict)
        for k in tweets:
            t = Tweet(tweets[k]['content'])
            if len(t.tokens):
                output = self.label_prevision_for_tweet(t.tokens)
            if output:
                # print output
                label = output['label']
                ratio = output['ratio']

            tweets[k]['sentiment'] = {'label' : label, 'certainty' : ratio}

        return tweets

    def label_prevision_for_tweet(self, tokens):
        try:
            case_positive = self.features['p(+)']
            case_negative = self.features['p(-)']
            prob_null_pos = 1000000*(1/ float((self.features['positive_tokens'] + self.features['total_tokens'])))
            prob_null_neg = 1000000*(1/ float((self.features['negative_tokens'] + self.features['total_tokens'])))

            tokens_dict = {} # Local dict to store the tweet's tokens

            for t in tokens: 
                try: #If tokens exist in global_dict
                    tokens_dict[t] = self.global_dict[t]
                    case_positive *= 1000000*tokens_dict[t]['p(+)']
                    case_negative *= 1000000*tokens_dict[t]['p(-)']
                
                except Exception as e: # Consider existence in dict as 0
                    case_positive *= prob_null_pos
                    case_negative *= prob_null_neg

            result = case_positive - case_negative
            # print result, prob_null_pos, prob_null_neg, case_negative, case_positive
            if result >= 0:
                label = 'positive'
            elif result < 0:
                label = 'negative'

            res_max = max(case_positive, case_negative)
            res_min = min(case_positive, case_negative)
            r = 1- res_min/float(res_max)
            ratio = '{:.2%}'.format(r)

            if (IS_POSSIBLY_UNDETERMINED and (r < CERTAINTY_RATE)):
                label = 'undetermined'

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            label = 'undetermined'
            ratio = 0


        results = {'label': label,'ratio': ratio}
        return results


if __name__ == '__main__':

    CLASSIFIER_FILE = 'classifier_global.json'
    FEATURES_FILE = 'features_global.json'
    tweets = {"815454904680521728":{"content":"Bush was so bad, we got to elect our 1st black president. After Trump, our president will be a 50 ft tall militant feminist Latina lesbian.","relations":[]},"815597538120241152":{"content":"Like any authoritarian, Trump undermines institutions, obscures the truth & promotes himself as its ultimate source. https:\/\/t.co\/XKRbLEdS8L","relations":[]},"815589456321409024":{"content":"\u05ea\u05d5\u05d3\u05d4 \u05e2\u05dc \u05ea\u05de\u05d9\u05db\u05ea\u05da \u05d4\u05e0\u05e9\u05d9\u05d0 \u05d4\u05e0\u05d1\u05d7\u05e8 \u05d8\u05e8\u05d0\u05de\u05e4! \ud83c\uddfa\ud83c\uddf8\ud83c\uddee\ud83c\uddf1\n\nThanks for your support, President-elect Trump! \ud83c\uddfa\ud83c\uddf8\ud83c\uddee\ud83c\uddf1\n\n@realDonaldTrump https:\/\/t.co\/4SOD9hVwCP","relations":[]},"815950948094902272":{"content":"RT @Jharman77: When you think you're bashing Trump, but end up describing literally exactly what Hillary Clinton, the person you supported,\u2026","relations":[]},"815950948031991813":{"content":"RT @thehill: Dem lawmaker: Voters will have \"buyers remorse\" over Trump https:\/\/t.co\/55RPRzmQDp https:\/\/t.co\/r5xgumDlxR","relations":[]},"815950948015210496":{"content":"RT @ThePlumLineGS: Yes, Trump \"lies.\" A lot. And news orgs should say so.\n\nA response to @WSJ editor-in-chief Gerard Baker:\n\nhttps:\/\/t.co\/e\u2026","relations":[]},"815950947864158208":{"content":"RT @igorvolsky: Editor of nation\u2019s second-biggest newspaper says he will not report Trump lies, even if he lie https:\/\/t.co\/CxzlvcZaBr","relations":[]},"815950947616694272":{"content":"RT @America_1st_: Sebastian Gorka: \"There's going to be a new sheriff in town called Donald Trump.\" https:\/\/t.co\/KEbxIjZ7j6","relations":[]},"815950946907918336":{"content":"RT @justkelly_ok: For folks across the US: Plan B is still available over the counter. Its shelf-life is four years. Trump takes office in\u2026","relations":[]},"815950946815459328":{"content":"RT @snarkytoes: @RxRantTweet @h4x354x0r @YouTube Yes! Very true. It is gut instinct, lizard brain stuff. Trump played so well to the tribal\u2026","relations":[]},"815950946777829377":{"content":"RT @ConversaAfiada: Nova e trepidante enquete do Conversa Afiada: Se o D\u00f3ria n\u00e3o \u00e9 o J\u00e2nio, o Justus, nem o Trump, o que ele \u00e9?\n\nVote: http\u2026","relations":[]}}

    # tweets = (sys.argv[1])
    # CLASSIFIER_FILE = str(sys.argv[2])
    # FEATURES_FILE = str(sys.argv[3])
    d = Classifier()


    labelled_tweets = d.make_labels(tweets)
    print labelled_tweets
