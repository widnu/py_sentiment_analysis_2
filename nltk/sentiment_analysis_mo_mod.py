# https://www.datacamp.com/community/tutorials/simplifying-sentiment-analysis-python
# Load and prepare the dataset
import random

from joblib import dump
from nltk.corpus import movie_reviews

import nltk

m_cat = movie_reviews.categories()
m_fileids = movie_reviews.fileids()
m_words = movie_reviews.words()

documents = [(list(movie_reviews.words(fileid)), category)
              for category in movie_reviews.categories()
              for fileid in movie_reviews.fileids(category)]

random.shuffle(documents)

# Define the feature extractor

all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_features = list(all_words)[:2000]

def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features

# Train Naive Bayes classifier
featuresets = [(document_features(d), c) for (d,c) in documents]
train_set, test_set = featuresets[100:], featuresets[:100]

classifier = nltk.NaiveBayesClassifier.train(train_set)

# Test the classifier
print(nltk.classify.accuracy(classifier, test_set))

##############################

def features(sentence):
     words = sentence.lower().split()
     return dict(('contains(%s)' % w, True) for w in words)

y_hat = features('Everything will be alright.')
y_pred = classifier.classify(y_hat)
print(y_pred)

y_hat = features('I do not like it')
y_pred = classifier.classify(y_hat)
print(y_pred)

##############################
# save model
dump(classifier, "nltk_sentiment_movie_review.joblib")

print("Save NLTK model successfully...")