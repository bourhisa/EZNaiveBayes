#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from __future__ import division

import os, json, csv, re, time
from random import shuffle
from random import randint
from config import *
from utilities import *
from labelled_classifier import LabelledClassifier
from item import Item


# This class manages all the operations related with a Dataset (either for training, testing or preparing the datasets)

class Dataset():
    items = []
    size = 0
    features = {}

    def __init__(self):
        self.items = []
        self.steps = 0
        self.size = 0
        self.features = {}

    # !! Considered the first function to use
    def import_from_csv(self, infile, **keyword_parameters):  # Imports CSV dataset and preprocesses the data
        # If 'nb' specified, import the given number of items. Otherwise, the whole.
        i = 0
        read_csv = csv.reader(open(infile, 'rb'), delimiter=',')

        dataset = [x for x in read_csv]
        shuffle(dataset) # Randomize the items so the testing/training samples are independent

        if 'nb' in keyword_parameters:
            dataset = dataset[:keyword_parameters['nb']]

        # Filters the items and cleans them
        for data in dataset:
            try:
                label = data[INDEX_LABEL]
                text = self.preprocess(data[INDEX_TEXT])
                if len(text) > 0:
                    self.items.append({'text': text, 'label': label})
            except:
                i += 1

        print_output("{:.2%} loss in the dataset due to encoding".format(i/float(len(dataset))))
        self.size = len(self.items)
        self.make_features_dataset()

    def import_from_json(self, infile, **keyword_parameters):  # Imports dataset from a JSON file
        # Option 'nb' to specify a number of items to import. Otherwise, imports the whole.

        data = json.loads(open(infile, 'r').read())
        shuffle(data)
        if 'nb' in keyword_parameters:
            data = data[:keyword_parameters['nb']]

        self.items = data
        self.size = len(self.items)
        self.make_features_dataset()

        msg = "Dataset of size {} generated".format(self.size)
        print_output(msg)

    def save(self, json_file):  # Save the dataset to JSON.
        with open(json_file, 'w+') as out:
            json.dump(self.items, out, indent=2, separators=(',', ': '))
        self.items = []

    def split(self, file_training, file_testing): # Splits into training and testing

            cut = int(CUT_RATIO * len(self.items))
            training = self.items[:cut]
            testing = self.items[cut:]

            for g in ["testing", "training"]:
                filename = eval("FILE_" + g.upper())

                with open(filename , 'w+') as out:
                    json.dump(eval(g), out, indent=2, separators=(',', ': '))

    # Clean the text data: lowercase, banalizes links and calls to other users, and deletes special chars
    def preprocess(self, item):
        try:
            item = unicode(item.lower())
            item = re.sub('\\n', '', item)  # gets rid of line breaks
            item = re.sub('@\S*', 'AT_USER', item)  # banalizes user references
            item = re.sub('https?://\S*', 'URL ', item)
            item = re.sub('www\S*', 'URL ', item)  # banalizes links
            # item = ' \u'.join(item.split('\\u')) # attempt to treat emojis
            item = re.sub("[@'\\$`,\-#%&;.:=()0]\/", '', item)
            return item
        except Exception as e:
            # print e, item
            pass

    def make_features_dataset(self):  # Calculates the rates for each label

        count_classifiers = {label: ([(label in t['label']) for t in self.items]).count(True) for label in LABELS}
        # count_classifiers = {label_1 : nb_items_with_label_1, label_2 : nb_items_with_label_2 , ....}

        nb = len(self.items)
        self.features = {label: count_classifiers[label] / float(nb) for label in LABELS}

    def build_classifiers(self):  # Sets up the counting operation

        labelled_classifiers = {label: LabelledClassifier(label, self.size) for label in LABELS}  # Initiates a dict with all the existing labels
        # labelled_classifiers =  {
        # label_1 : LabelledClassifier_with_label_1
        # label_2 : LabelledClassifier_with_label_2
        # ... }

        steps = int(round(len(self.items) / 13, 0))
        item_queue = self.items
        time_start = time.time()  # Measures the overall time
        i = 0

        print_output('Building classifiers...')

        for t in item_queue:
            item = Item(t)
            label = item.label.encode('utf-8')

            if label not in LABELS:
                LABELS.append(label)
                labelled_classifiers[label] = LabelledClassifier(label, self.size)

            labelled_classifiers[label].add_item_to_classifier(item.tokens)
            del item

            i += 1

            if i % steps == 0 or i == len(item_queue):  # Repeats at every step and at the end of execution
                time_queue = time.time()

                for c in labelled_classifiers.values():
                    c.update_classifier()
                    c.save_classifier_to_file()

                proportion_done = round(i / self.size, 2)
                print_loading("Items tokenized: ", proportion_done, self.size - i, "All items tokenized")

        msg = 'Took a total of {} seconds, or {} per item'.format(time.time() - time_start,
                                                                   (time.time() - time_start) / float(self.size))
        print_output(msg)

        for c in labelled_classifiers.values():
            del c

        item_queue = []
