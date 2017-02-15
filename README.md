# EZNaiveBayes

Python NaiveBayes classifier for text classification.
This project intends to be working flawlessly on every labelled text dataset, it is full-featured and easy to use.

This classifier was originally developped to perform sentiment analysis on a dataset from Twitter with binary labels (positive/negative). 
It has been adapted to manage automatically as many labels as there are.

It takes as an input any CSV file of labelled text data.
It outputs exportable JSON NaiveBayes classifiers, and an Excel file containing all the testing results to compare and chose the  best classifier.
It has been developped so the user can set everything via the config.py file and fire the program.

It takes in charge:
- Dataset preparation, cleaning, filtering and repartition between training & testing datasets.
- Creation of randomized independent datasets to build and test the classifiers
- Tokenization of the text with many options
- Gathering and calculations of all the necessary features
- Generation of exportable JSON files
- Application of the classifier to a test dataset
- Formatted output of the test including many info to pick the dataset you need
- Production file callable from external scripts to classify items based on the trained classifiers

Once you have your CSV dataset, it takes only 5 steps from download to production, by  from only 2 files

- 1. Installation
Download the library
Install all the required packages and libraries

- 2. Setup
Go to config.py and set all the variables to fit your needs and your dataset.

- 3. Dataset preparation
Inside NaiveBayes.py, uncomment the first phase, called "init_datasets"

- 4. Training & Testing
Run NaiveBayes.py, it will train and test all the samples you specified in config.py

- 5. Production
Place the sentiment_analysis.py in your folder, adapt the global variables to your needs and your scripts.

Enjoy, please send me your feedbacks!
