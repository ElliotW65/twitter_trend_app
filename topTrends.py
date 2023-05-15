import json
import sys
import tweepy
from collections import Counter
import json
from geopy.geocoders import Nominatim


# keys for accessing api

access_key  = '1355462078526586881-K9VpsFZyoFGDChTkPM300iUD2Nq4Ys'
access_secret = 'k1KM7lQcThAiBz1YNixMWb8n67vVYMotFqOZTQY41Ravj'
consumer_key = 'Ay5TPFHwmPADMHEt6dTUaFiQz'
consumer_secret = 'FWVBDmeOq4Lj6krXDKsh0Tz7lgCNFBpmQtFBwaCgkY9Mf9lcwb'


#setting up access of api using keys

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

tweet_text_list = []
hashtag_list = []

sample = [('#sportingsempre', 1), ('#sportingcp', 1), ('#sportingtoronto', 1), ('#Toronto,', 1), ('#Retail', 1)]


#returns tweets as JSON Objects in a radius from the coordinate argument passed

def tweets_from_coordinates(x, y):
    tweet_geocode = str(x) + "," + str(y) + ",5km"
    return api.search(geocode=tweet_geocode, count = 1000, tweet_mode = 'extended')


#filters out text body of tweets from JSON objects and adds them to tweet_text_List

def tweets_text_list(x):
    tweet_text_list.clear()
    for i in x:
        tweet_text_list.append(str(i.full_text))
    return tweet_text_list


#filters out hashtags from tweet text body and adds them to hashtag_list

def hashtags_from_tweets(s):
    hashtag_list.clear()
    for i in s:
        hashtag_list.extend(word for word in i.split() if word.startswith('#'))
    return hashtag_list


#Finds the top five most common hashtags from  the hashtag_list

def most_common_hashtags(t):
    for x in t:
        top_five_hashtags = Counter(t).most_common(5)
    return top_five_hashtags


# print(json_convert(sample))

def json_convert(j):
    json_out = []
    for i in j:
        item = {"tag": i[0], "count": i[1]}
        json_out.append(item)
    data = json.dumps(json_out)
    return data

hashtags_from_tweets(tweets_text_list(tweets_from_coordinates(sys.argv[1], sys.argv[2])))

# print(sys.argv[1], sys.argv[2])
print(json_convert(most_common_hashtags(hashtag_list)))
