#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from __future__ import division

# Training factors

# Operations in cleaning
RANDOM_ELIMINATOR = True  # If a token appears only once in the training dataset, do NOT consider it valid => filesize/5
DELETE_STOPWORDS = False  # Delete non-semantic words such as 'a, the, my, is'
STEMMING = False  # 'Have, had, has, having' all become 'have' => not 100% benefic and takes time

# Tokens selection: which token to take in consideration?
TWO_CONSECUTIVE = True  # (n, n+1)
TWO_AHEAD = True  # (n, n+2)
THREE_CONSECUTIVE = False # (n, n+1, n+1+2)
TWO_RANDOM = False # All the combinations of 2 words within the phrase

# Dataset parameters

DATASET_PATH = 'datasets/demo/'  # Where the datasets are stored
ORIGINAL_CSV = DATASET_PATH + 'sentiment_analysis_dataset.csv'  # Original CSV  file
FILE_JSON = DATASET_PATH + 'subs/sentiment_analysis_dataset.json'  # Optional JSON file. Cleaned version of the CSV
FILE_TRAINING = DATASET_PATH + 'subs/sentiment_analysis_dataset_training.json' # Training set, all classifiers built upon this one
FILE_TESTING = DATASET_PATH + 'subs/sentiment_analysis_dataset_testing.json'  # Testing set, where the test items will be picked

CLASSIFIER_PATH = DATASET_PATH + 'classifiers/'  # Location of classifiers + results file
SAMPLE_PATH = CLASSIFIER_PATH + '{}_sample/' # Individual location pattern of every classifier

LABELLED_CLASSIFIER_FILENAME = SAMPLE_PATH + '{}_labelled_classifier_{}' # Name pattern of the labelled classifiers
FEATURES_FILENAME = SAMPLE_PATH + '{}_features_global.json' # Name pattern for the features file of every classifier
GLOBAL_CLASSIFIER_FILENAME = SAMPLE_PATH + '{}_classifier_global.json' # Name pattern for the global classifier

INDEX_LABEL = 1 # Index of the label in the CSV  input
INDEX_TEXT =  3 # Index of the text

CUT_RATIO = 2/3  # Repartition ratio between training and testing datasets

# Testing options
CONSOLE_OUTPUTS = True  #  Write console outputs?
IS_POSSIBLY_UNDETERMINED = True  # Under a certain percentage of certainty, label 'undetermined'
UNDETERMINATION_RATES = [0, 0.15, 0.3, 0.5] # Under which rates
PERSISTENCY_RESULTS = True  # Write the outputs in a file?
CONSOLE_RESULTS = False  # Write output in console?

LIST_SAMPLES = [11000]  # Sizes of the different classifiers
TO_BE_TRAINED = LIST_SAMPLES # Samples to be trained
TO_BE_TESTED = [1000, 5000, 8000, 50000, 500000,1000000]# Samples to be tested

LABELS = []  # List of all labels found in the training dataset, fills itself automatically

SIZE_OF_SAMPLE_TEST = 1000  # Number of items used to run the test

tokenization_options = [] # String to be output either in the console or in the results file
if RANDOM_ELIMINATOR:
    tokenization_options.append('Random eliminator')

if DELETE_STOPWORDS:
    tokenization_options.append('No stopwords')

if STEMMING:
    tokenization_options.append('Stemming')

if TWO_CONSECUTIVE:
    tokenization_options.append('2-Consecutive')

if TWO_AHEAD:
    tokenization_options.append('2 ahead')

if THREE_CONSECUTIVE:
    tokenization_options.append('3-Consecutive')

if TWO_RANDOM:
    tokenization_options.append('All bigrams')

TOKENIZATION_CHOICE = ', '.join(tokenization_options)
