import json
import sys
import tweepy
from collections import Counter
import json
from geopy.geocoders import Nominatim


# keys for accessing api

access_key  = '1366440159273713671-oANva7ClFbovtPGkXae5I4wCxaxrie'
access_secret = 'v4DJH6xvNs6mZhsmaw9manqRXOC8EccPMyZUF0ET0QzMV'
consumer_key = 'wRpataioBhMHrhFFFOXUP1Z1N'
consumer_secret = '0Yb7mVt2ssVseh2GjcPhPbempSo5zv7dxJyxmhYcTFEM9YFOeT'


#setting up access of api using keys

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

tweet_text_list = []
hashtag_list = []

sample = [('#sportingsempre', 1), ('#sportingcp', 1), ('#sportingtoronto', 1), ('#Toronto,', 1), ('#Retail', 1)]

#geolocator used to find coordinates from an address
geolocator = Nominatim(user_agent = "trendy")


#function returns coordinates using geolocator

def coordinates_from_location(x):
    location = geolocator.geocode(x)
    return location.latitude, location.longitude


#returns tweets as JSON Objects in a radius from the coordinate argument passed

def tweets_from_coordinates(x, y):
    tweet_geocode = str(x) + "," + str(y) + ",1km"
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

def json_convert(j):
    json_out = []
    for i in j:
        item = {"tag": i[0], "count": i[1]}
        json_out.append(item)
    data = json.dumps(json_out)
    return data


# print(tweets_from_coordinates(coordinates_from_location(sys.argv)[0],coordinates_from_location(sys.argv)[1]))

# print(sys.argv[1])

hashtags_from_tweets(tweets_text_list(tweets_from_coordinates(coordinates_from_location(sys.argv[1])[0],coordinates_from_location(sys.argv[1])[1])))

print(json_convert(most_common_hashtags(hashtag_list)))
# print(sys.argv[1], sys.argv[2])
