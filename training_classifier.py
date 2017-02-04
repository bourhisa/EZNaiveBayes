#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from __future__ import division


import os, time, json
from collections import Counter

from config import *
from utilities import *
from item import Item
import operator

from labelled_classifier import LabelledClassifier


class TrainingClassifier():
    dicts = {label: '' for label in LABELS}
    global_dict = {}
    features = {}
    features_filename = ''
    classifier_filename = ''
    dataset = []
    size = ''
    i = ''

    def __init__(self, **keyword_parameters):

        if ('dataset' in keyword_parameters):
            self.dataset = keyword_parameters['dataset']
            self.size = len(self.dataset.items)
            self.i = self.size

        if ('size' in keyword_parameters):
            self.size = keyword_parameters['size']

        self.import_global_dict()

    def import_global_dict(self):  # Imports the previous information, or creates blank files and variables
        self.features_filename = FEATURES_FILENAME.format(self.size, self.size)
        self.classifier_filename = GLOBAL_CLASSIFIER_FILENAME.format(self.size, self.size)

        # Classifier file
        with open(self.classifier_filename, 'r') as f:
            try:
                self.global_dict = Counter(json.loads(p=f.read()))
            except:
                self.global_dict = Counter(dict())
            f.close()

        # Insights file
        with open(self.features_filename, 'r') as f:
            if f:
                try:
                    self.features = json.loads(p=f.read())
                except:
                    self.features = dict()
            f.close()

        msg = 'Global classifier info recovered'
        print_output(msg)

    def build(self):  # Calls all the functions required to train the classifier and build all the information
        self.import_labelled_classifiers()
        self.concatenate_tokens()
        self.get_tokens_features()
        self.make_probs()
        self.save_classifier_to_file()

    def import_labelled_classifiers(self):  # Import the LabelledClassifiers related to this dataset
        for label in LABELS:
            self.dicts[label] = LabelledClassifier(label, self.size).return_classifier_content()

        msg = 'Labelled classifiers imported'
        print_output(msg)

    def concatenate_tokens(self):  # Merges the counts for every token
        global_count = Counter()
        for label in LABELS:
            global_count += self.dicts[label]
        i = 0

        for k in global_count:
            if (RANDOM_ELIMINATOR == False) or (RANDOM_ELIMINATOR and global_count[k] > 1):  #
                self.global_dict[k] = {}
                self.global_dict[k]['NB_TOTAL'] = global_count[k]

                for label in LABELS:
                    try:
                        self.global_dict[k]["NB_" + label] = self.dicts[label][k]
                    except:
                        self.global_dict[k]["NB_" + label] = 0

            i += 1
            if i % 10000 == 0 or i == len(global_count):
                proportion_done = i / len(global_count)
                print_loading("Aggregating tokens: ", proportion_done, len(global_count) - i,
                              'Tokens concatenated and counted')

    def get_tokens_features(self):  # Calculates all the insights for the datasets
        self.features['tokens'] = {label: sum([int(x["NB_" + label]) for x in self.global_dict.values()]) for label in
                                   LABELS}
        self.features['tokens']['unique'] = len(self.global_dict.keys())
        self.features['tokens']['total'] = sum([int(x['NB_TOTAL']) for x in self.global_dict.values()])
        self.features['labels'] = LABELS
        self.dataset.make_features_dataset()
        self.features['probs'] = self.dataset.features
        # self.features.update(self.dataset.features)
        msg = 'Classifier features calculated'
        print_output(msg)

    def save_classifier_to_file(self):  # Writes the classifier in json ouput
        try:
            with open(self.classifier_filename, 'w') as f:
                json.dump(self.global_dict, f, indent=2, separators=(',', ': '))
                f.close()
                with open(self.features_filename, 'w') as f:
                    json.dump(self.features, f, indent=2, separators=(',', ': '))
                    f.close()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

            msg = 'Classifier saved'
            print_output(msg)

    def make_probs(self):  # Calculates the probabilities to find token t for a item of a certain label
        i = 0
        len_keys = len(self.global_dict.keys())
        for k in self.global_dict.keys():
            for label in LABELS:
                self.global_dict[k]['P' + label] = float('{:01.12f}'.format(round(
                    (self.global_dict[k]["NB_" + label] + 1) \
                    / (self.features['tokens'][label] + self.features['tokens']['total'])
                    , 12)))

            i += 1
            if i % 50000 == 0 or i == len_keys:
                proportion_done = i / float(len_keys)
                print_loading('Probabilities:', proportion_done, len_keys - i, "Probabilities made")
