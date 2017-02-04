#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import  os, json
from collections import Counter
from config import *


class LabelledClassifier():  # Manages I/O and update of classifier files

    filename = ''
    classifier_from_file = Counter()  # Contains all the counts
    token_chain = Counter()  # Big chain with all the tokens to be counted

    def __init__(self, label, nb):
        self.get_classifier_file(label, nb)
        self.read_classifier()
        self.token_chain = []

    def get_classifier_file(self, label , nb):

        self.filename = LABELLED_CLASSIFIER_FILENAME.format(nb, nb, label)

        if not os.path.isfile(self.filename):
            f = open(self.filename, 'w').close()

    def read_classifier(self):
        with open(self.filename, 'r') as f:
            p = f.read()
            if f:
                try:
                    self.classifier_from_file = Counter(json.loads(p))
                except:
                    self.classifier_from_file = Counter()
            f.close()

    def add_item_to_classifier(self, tokens_bag):  # Adds all the new tokens to the previous list
        self.token_chain += tokens_bag

    def update_classifier(self):  # Counts the new tokens and merge with previous counts
        self.classifier_from_file += Counter(self.token_chain)
        self.token_chain = []

    def return_classifier_content(self):  # Return classifier
        return self.classifier_from_file

    def save_classifier_to_file(self):  # Writes the classifier in json ouput
        with open(self.filename , 'w') as f:
            json.dump(dict(self.classifier_from_file), f, indent=2, separators=(',', ': '))
        f.close()

    def __del__(self):
        self.update_classifier()
        self.save_classifier_to_file()
        classifier_from_file = []