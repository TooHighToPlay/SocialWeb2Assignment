import requests
from pprint import pprint
import json
import sys

SENTIMENT = {
    0: 'negative',
    2: 'neutral',
    4: 'positive'
}

URL = 'http://www.sentiment140.com/api/bulkClassifyJson?appid=mihnea@linux.com'



def make_request(tweets):
    body = {'data': tweets}
    response = requests.post(URL, data=json.dumps(body))
    return response

def process_response(response):
    data = response.json()['data']
    for tweet in data:
        tweet['sentiment'] = SENTIMENT[tweet['polarity']]
    return data

def process_sentiments(data):
    sentiments = {}
    for tweet in data:
        if tweet['country_code'] not in sentiments:
            sentiments[tweet['country_code']] = {
                'negative': 0,
                'positive': 0,
                'neutral': 0
            }
        s = tweet['sentiment']
        sentiments[tweet['country_code']][s] += 1

    return sentiments

def calculate_ratio(sentiments):
    new_sentiments = {}
    for country in sentiments:
        new_sentiments[country] = (((-1. * sentiments[country]['negative'] + \
                sentiments[country]['positive']) / \
                (sentiments[country]['negative'] + \
                sentiments[country]['positive'] + \
                sentiments[country]['neutral'])) + 1) * 5
    return new_sentiments


if __name__ == '__main__':
    items = []
    with open(sys.argv[1]) as f:
        for line in f:
            item = json.loads(line.strip())
            items.append(item)
    data = process_response(make_request(items))
    sentiments = process_sentiments(data)
    computed_sentiments = calculate_ratio(sentiments)

    print json.dumps(computed_sentiments, indent=2)

