import tweepy
from collections import Counter
import json
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
import numpy as np

access_key  = '1366440159273713671-oANva7ClFbovtPGkXae5I4wCxaxrie'
access_secret = 'v4DJH6xvNs6mZhsmaw9manqRXOC8EccPMyZUF0ET0QzMV'
consumer_key = 'wRpataioBhMHrhFFFOXUP1Z1N'
consumer_secret = '0Yb7mVt2ssVseh2GjcPhPbempSo5zv7dxJyxmhYcTFEM9YFOeT'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

geolocator = Nominatim(user_agent = "trendy")


hashtag_list = []

def hashtags_from_tweets(s):
    hashtag_list.clear()
    for i in s:
        hashtag_list.extend(word for word in i.split() if word.startswith('#'))
    return hashtag_list


def most_common_hashtags(t):
    for x in t:
        top_five_hashtags = Counter(t).most_common(5)
    return top_five_hashtags


def tweets_from_coordinates(x, y):
    tweet_geocode = str(x) + "," + str(y) + ",5km"
    return api.search(geocode=tweet_geocode, count = 1000, tweet_mode = 'extended')


def coordinates_from_location(x):
    location = geolocator.geocode(x)
    return location.latitude, location.longitude


tweet_text_list = []

def tweets_text_list(x):
    tweet_text_list.clear()
    for i in x:
        tweet_text_list.append(str(i.full_text))
    return tweet_text_list


def hashtag_percentages(x):
    total_tweets = 0
    top_hashtag_percentages = []
    for i in x:
        total_tweets += i[1]
    for i in x:
        top_hashtag_percentages.extend((i[0],(round(i[1]/total_tweets,4)*100)))
    return top_hashtag_percentages


def top_five_hashtags(location = 'Default', x = 'Default', y = 'Default'):
    if location == 'Default':
        coord_hashtags = most_common_hashtags(hashtags_from_tweets(tweets_text_list(tweets_from_coordinates(x, y))))
        percent_hashtags = hashtag_percentages(coord_hashtags)
        return coord_hashtags
    elif x == 'Default' or y == 'Default':
        x = coordinates_from_location(location)[0]
        y = coordinates_from_location(location)[1]
        coord_hashtags = most_common_hashtags(hashtags_from_tweets(tweets_text_list(tweets_from_coordinates(x, y))))
        percent_hashtags = hashtag_percentages(coord_hashtags)
        return coord_hashtags


def top_five_hashtags_graph(hashtag_list):
    top_five = hashtag_list
    y = np.array([top_five[0][1], top_five[1][1], top_five[2][1], top_five[3][1], top_five[4][1]])
    mylabels = [top_five[0][0] + " - " + str(top_five[0][1]), top_five[1][0] + " - " + str(top_five[1][1]), top_five[2][0] + " - " + str(top_five[2][1])
                , top_five[3][0] + " - " + str(top_five[3][1]), top_five[4][0] + " - " + str(top_five[4][1])]

    plt.pie(y, labels = mylabels)
    plt.show() 
