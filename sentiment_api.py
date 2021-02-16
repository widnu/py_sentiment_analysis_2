# https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask

# cd C:\dev\nz\git\vr_sentiment_analysis
# python sentiment_api.py
# http://127.0.0.1:5000/
# http://127.0.0.1:5000/api/v1/resources/sentiment/mo
# http://127.0.0.1:5000/api/v1/resources/sentiment/tw
# http://127.0.0.1:5000/api/v1/resources/sentiment/vader
# http://127.0.0.1:5000/api/v2/resources/sentiment/vader

import json
import re
import string

import flask
from chatterbot import ChatBot
from flask import request
from joblib import load
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

app = flask.Flask(__name__)
app.config["DEBUG"] = True

##################################################
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Welcome to Sentiment Analysis APIs</h1>
<p>implemented by nltk</p>'''

##################################################
def remove_noise(tweet_tokens, stop_words = ()):
    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())

    return cleaned_tokens

##################################################
def features(sentence):
     words = sentence.lower().split()
     return dict(('contains(%s)' % w, True) for w in words)

##################################################
@app.route('/api/v1/resources/sentiment/mo', methods=['POST'])
def api_sentiment_movie_review():
    json_data = request.json
    sentence = json_data["sentence"]

    # load and predict - nltk movie_reviews
    classifier = load("nltk_sentiment_movie_review.joblib")
    y_hat = features(sentence)
    y_pred = classifier.classify(y_hat)
    print("movie_reviews: y_pred = " + y_pred)
        
    # json response via REST APIs
    result = json.dumps({
        'sentence': sentence, 
        'emotion': y_pred
        })
    print(result)
    return result

##################################################
@app.route('/api/v1/resources/sentiment/tw', methods=['POST'])
def api_sentiment_twitter():
    json_data = request.json
    sentence = json_data["sentence"]

    # load and predict - nltk twitter_samples
    classifier = load("nltk_sentiment_twitter.joblib")
    custom_tokens = remove_noise(word_tokenize(sentence))
    y_pred = classifier.classify(dict([token, True] for token in custom_tokens))
    print("twitter_samples: y_pred = " + y_pred)
    
    # json response via REST APIs
    result = json.dumps({
        'sentence': sentence, 
        'emotion': y_pred
        })
    print(result)
    return result
		
##################################################

from nltk.sentiment.vader import SentimentIntensityAnalyzer

@app.route('/api/v1/resources/sentiment/vader', methods=['POST'])
def api_sentiment_vader():
    json_data = request.json
    sentence = json_data["sentence"]

    # load and predict - nltk vader
    sid = SentimentIntensityAnalyzer()
    print(sentence)
    ss = sid.polarity_scores(sentence)
    print(ss)
    
    y_pred = 'Neutral'

    if ss['compound'] > 0:
        y_pred = 'Positive'
    else:
        y_pred = 'Negative'
    
    # json response via REST APIs
    result = json.dumps({
        'sentence': sentence, 
        'emotion': y_pred
        })
    print(result)
    return result

##################################################
@app.route('/api/v2/resources/sentiment/vader', methods=['POST'])
def api_sentiment_vader_with_neutral():
    json_data = request.json
    sentence = json_data["sentence"]

    # load and predict - nltk vader
    sid = SentimentIntensityAnalyzer()
    print(sentence)
    ss = sid.polarity_scores(sentence)
    print(ss)
    
    y_pred = 'Neutral'

    ss_compound = ss['compound']
    ss_pos = ss['pos']
    ss_neu = ss['neu']
    ss_neg = ss['neg']

    if ss_compound >= 0.5:
        y_pred = 'Positive'
    elif ss_compound <= -0.5:
        y_pred = 'Negative'
    else:
        y_pred = 'Neutral'

    # if ss_pos > ss_neu and ss_pos > ss_neg:
    #     y_pred = 'Positive'
    # elif ss_neu > ss_pos and ss_neu > ss_neg:
    #     y_pred = 'Neutral'
    # elif ss_neg > ss_pos and ss_neg > ss_neu:
    #     y_pred = 'Negative'
    
    # json response via REST APIs
    result = json.dumps({
        'sentence': sentence, 
        'emotion': y_pred
        })
    print(result)
    return result

##################################################
@app.route('/api/v2/resources/chatbot', methods=['POST'])
def api_chatbot():
    json_data = request.json
    sentence = json_data["sentence"]
    print("input:", sentence)

    bot = ChatBot('Buddy')
    
    # Create a new trainer for the chatbot
    # trainer = ChatterBotCorpusTrainer(bot)
    # trainer.train("./chatbot/corpus/")
    
	# Get a response to the input text 'I would like to book a flight.'
    bot_response = bot.get_response(sentence)
    print("Bot reply:", bot_response)

    # json response via REST APIs
    result = json.dumps({
        'bot_sentence': str(bot_response)
        })
    print(result)
    return result
	
##################################################

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)