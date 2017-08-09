#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from __future__ import division

# This library has been designed to train a NaiveBayes Classifier out of a CSV or JSON file.
# It returns a trained classifier in JSON for exportation purposes.
# It needs adaptation in order to manage a different set of labels
# The management of various dataset files has been implemented

import sys

reload(sys)
sys.setdefaultencoding('utf8')
import time, re, itertools, json, pprint, os, csv, math, pprint
from random import randint
from collections import Counter
from decimal import *

# Classes from this library
from config import *
from utilities import *
from labelled_classifier import LabelledClassifier
from training_classifier import TrainingClassifier
from testing_classifier import TestingClassifier
from item import Item
from dataset import Dataset

def init_datasets(csv, training, testing):  # First procedural function. Imports from the CSV, and sets up the datasets
    init_files()
    x = Dataset()
    x.import_from_csv(csv)
    print_output("Dataset imported from the original CSV")

    x.split(FILE_TRAINING, FILE_TESTING)
    x.save(FILE_JSON)
    print_output("JSON datasets generated")


def train(size):  # Trains a classifier of the specified size

    print_output("\n Training set {} \n {}".format(size, '-' * 40))

    d = Dataset()

    d.import_from_json(FILE_TRAINING, nb = size)
    d.build_classifiers()  # Fills LabelledClassifiers

    t = TrainingClassifier(dataset = d, size = size)
    t.build()  # Concatenates counts and probs for every token


def test(sample_size):  # Tests a given classifier for different
    for r in UNDETERMINATION_RATES:

        print_output("\n Testing set {} for rate {} \n {}".format(sample_size, r, '-' * 40))

        start = time.time()

        test = Dataset()
        test.import_from_json(FILE_TESTING, nb = SIZE_OF_SAMPLE_TEST)  #  Creates the test dataset
        t = TestingClassifier(dataset = test, size = sample_size)

        t.make_test(r, start)

        end = time.time()

        print_output( "Tested in {} seconds".format(end - start))


if __name__ == '__main__':

    print_output(TOKENIZATION_CHOICE)

    init_files()

    #init_datasets(ORIGINAL_CSV, FILE_TRAINING, FILE_TESTING)

    for sizes in TO_BE_TRAINED:
        train(sizes)

    for sizes in TO_BE_TESTED:
        test(sizes)
