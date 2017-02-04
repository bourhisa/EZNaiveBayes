#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from __future__ import division


import os, time, json
from collections import Counter

from config import *
from utilities import *
from item import Item
import operator


class TestingClassifier():

    results = []
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

# Imports the previous information, or creates blank files and variables
    def import_global_dict(self):

        self.features_filename = FEATURES_FILENAME.format(self.size, self.size)
        self.classifier_filename = GLOBAL_CLASSIFIER_FILENAME.format(self.size, self.size)

        # Classifier file
        # if not os.path.isfile(self.classifier_filename):
        #     f = open(self.classifier_filename, 'w').close()
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
                    self.features = { k.encode('utf-8') : v for k, v in json.loads(p).items()}
                    LABELS = [l.encode('utf-8') for l in self.features['labels']]
                except:
                    self.features = dict()

            f.close()
        msg = 'Global classifier info recovered'
        print_output(msg)


# Manages the test for the dataset
    def make_test(self, certainty_rate, time_start):
        undetermined_results = []
        test_results = []
        printable_results = []
        self.global_dict = dict(self.global_dict)
        i = 0
        start_queue = time.time()
        nb_tokens = 0
        for item in self.dataset.items:
            	i += 1
                try:
                    t = Item(item)
                    expected_label = t.label
                    if len(t.tokens):
                        output = self.label_prevision_for_item(t.tokens, certainty_rate)
                    if output:
                        ratio = output['ratio']
                        predicted_label = output['label']
                        if predicted_label != 'undetermined':
                            if predicted_label == expected_label:
                                test_results.append(1)
                            else:
                                test_results.append(0)
                        else:
                            undetermined_results.append(1)


                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    # print(exc_type, fname, exc_tb.tb_lineno), item
                    undetermined_results.append(1)

                nb_tokens += len(t.tokens)

                if i % 1000 == 0 or i == len(self.dataset.items):
                    elapsed_queue = round(time.time()- start_queue, 2)
                    elapsed_test =  round(time.time()- time_start, 2)
                    proportion_done = i/float(len(self.dataset.items))
                    print_loading("items tested: ", proportion_done, len(self.dataset.items) - i, "All items tested")


        if PERSISTENCY_RESULTS or CONSOLE_RESULTS:
            output = []
            output.append(TOKENIZATION_CHOICE)
            output.append(self.size) # Sample tested
            output.append(certainty_rate) # Certainty rate applied
            output.append('{:.2%}'.format(sum(test_results)/ float(len(test_results)))) #  Accuracy
            output.append('{:.2%}'.format(sum(undetermined_results)/float(i)))   # Undetermined rate
            output.append(nb_tokens/float(i)) # Avg nb of tokens per item
            output.append(elapsed_queue/float(len(self.dataset.items))) # Testing time per item
            output.append(elapsed_test)
            output.append('{:.2%}'.format((len(test_results)+len(undetermined_results))/float(i))) # %items passed
            output.append(round(os.path.getsize(self.classifier_filename)/float(1000000),2)) # Filesize of the sample
            output.append(len(self.dataset.items))
            output = [str(x) for x in output] 
            self.print_results(output)

# Called by make_test(), makes the prediction about the label and the confidence ratio for one item
    def label_prevision_for_item(self, tokens, certainty_rate):

        try:
            case_labels = {label : self.features['probs'][label] for label in LABELS}
            case_nulls = {label : 1000000*(1/ float((self.features['tokens'][label] + self.features['tokens']['total']))) for label in LABELS}
            tokens_dict = {} # Local dict to store the item's tokens

            for t in tokens:
                try: #If tokens exist in global_dict
                    tokens_dict[t] = self.global_dict[t]
                    for label in LABELS:
                        case_labels[label] *= 1000000*tokens_dict[t]['P' + label]

                except Exception as e: # Consider existence in dict as 0
                    for label in LABELS:
                        case_labels[label] *= case_nulls[label]

            result = max(case_labels.values())
            label = max(case_labels.iteritems(), key=operator.itemgetter(1))[0]

            r = result/float(sum(case_labels.values()))
            ratio = '{:.2%}'.format(r)

            if (IS_POSSIBLY_UNDETERMINED and (r < certainty_rate)):
                label = 'undetermined'

            results = {'label': label,'ratio': ratio}
            return results
        except Exception as e:
            print e

# Manages the output in tsv
    def print_results(self, output):
        outfile = CLASSIFIER_PATH + 'results.tsv'
        results_file = outfile
        # if not os.path.isfile(results_file):
        #     f = open(results_file, 'w').close()

        with open(results_file, 'r') as f:
            if f:
                self.results = [x.split('\t') for x in f.read().split('\n')]
                if len(self.results) < 2 :
                    self.results = [['Tokenization', '#Training items', 'Determination rate', 'Accuracy', 'Uncertainty rate', 'Tokens/item',\
                    'Time/item', 'Duration of test', 'items passed', 'Weight file (MB)', 'Size of test panel']]
            f.close()

        self.results.append(output)

        printable_results = '\n'.join(['\t'.join(x) for x in self.results])
        
        if PERSISTENCY_RESULTS:
            with open(outfile, 'w') as p:
                p.write(printable_results)

        if CONSOLE_RESULTS:
            print (printable_results)