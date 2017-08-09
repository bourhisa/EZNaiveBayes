#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import sys, os
from config import *


def print_loading(label, proportion, remaining, end):  # Prints a loading bar
    to_be_printed = "\r" + label
    nb_symbols = int(round((proportion*40),0))
    to_be_printed += " [{}{}] {:.2%}, {} remaining".format("#" * nb_symbols, " "* (int(40)-nb_symbols), proportion, remaining)
    sys.stdout.write(to_be_printed)
    sys.stdout.flush()
    if proportion == 1:
        print "\r " + end


def print_output(msg):  # Prints console outputs
    if CONSOLE_OUTPUTS:
        print (msg)


def init_files():
    for filename in [FILE_TESTING, FILE_TRAINING, FILE_JSON]:
        if not os.path.exists(filename):
            if len(filename.split('/')) > 1:
                if not os.path.exists('/'.join(filename.split('/')[:-1])):
                    os.makedirs('/'.join(filename.split('/')[:-1]))

            open(filename, 'w').close()

    for sample_size in LIST_SAMPLES:
        path = SAMPLE_PATH.format(sample_size)
        if not os.path.exists(path):
            os.makedirs(path)

        for f in [GLOBAL_CLASSIFIER_FILENAME, FEATURES_FILENAME]:
            filename = f.format(sample_size, sample_size)
            if not os.path.exists(filename):
                open(filename, 'w').close()

    results_file = CLASSIFIER_PATH  + 'results.tsv'
    if not os.path.exists(results_file):
        open(results_file, 'w').close()




