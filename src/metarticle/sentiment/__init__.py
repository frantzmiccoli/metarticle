import os
import pickle

from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer, sent_tokenize

from metarticle import cacheutil

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
            features = extract_features(sentence)
            output.append((features, label))

def train_sentiment_classifier():
    training_set = []
    load_samples('../data/train/neg', 'neg', training_set)
    load_samples('../data/train/pos', 'pos', training_set)
    return NaiveBayesClassifier.train(training_set)

def get_sentiment(text):
    features = extract_features(text)
    dist = get_sentiment_classifier().prob_classify(features)
    if dist.prob('neg') >= 2./3.:
        return 'negative'
    elif dist.prob('pos') >= 2./3.:
        return 'positive'
    else:
        return 'neutral'

classifier_path = '../data/classifier.model'

_sentiment_classifier = None


def get_sentiment_classifier():
    global _sentiment_classifier
    if _sentiment_classifier is None:
        _sentiment_classifier = cacheutil.get_from_cache(classifier_path)
    if _sentiment_classifier is None:
        _sentiment_classifier = train_sentiment_classifier()
        cacheutil.store_in_cache(classifier_path, _sentiment_classifier)
    return _sentiment_classifier
