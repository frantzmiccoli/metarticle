import os

import nltk
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer, sent_tokenize

def extract_features(text):
    splitter = RegexpTokenizer(r'\w+')
    
    words = {}
    for word in splitter.tokenize(text):
        if word not in stopwords.words():
            words[word.lower()] = 1
    
    return words

# Setup naive bayes classifier for sentiment analysis
def load_samples(path, label, output):
    for f in os.listdir(path):
        fullpath = path + '/' + f
        print fullpath
        data = open(fullpath).read()
        for sentence in sent_tokenize(data):
            features = extract_features(data)
            output.append((features, label))

def train_sentiment_classifier():
    training_set = []
    load_samples('../data/train/neg', 'neg', training_set)
    load_samples('../data/train/pos', 'pos', training_set)
    return NaiveBayesClassifier.train(training_set)

sentiment_classifier = train_sentiment_classifier()

def get_sentiment(text):
    features = extract_features(text)
    dist = sentiment_classifier.prob_classify(features)
    if dist.prob('neg') >= 2./3.:
        return 'negative'
    elif dist.prob('pos') >= 2./3.:
        return 'positive'
    else:
        return 'neutral'

