#!/usr/bin/env python
# coding: utf-8

# In[8]:


import tweepy
from collections import Counter
import json
from geopy.geocoders import Nominatim



# In[9]:


access_key  = '1366440159273713671-oANva7ClFbovtPGkXae5I4wCxaxrie'
access_secret = 'v4DJH6xvNs6mZhsmaw9manqRXOC8EccPMyZUF0ET0QzMV'
consumer_key = 'wRpataioBhMHrhFFFOXUP1Z1N'
consumer_secret = '0Yb7mVt2ssVseh2GjcPhPbempSo5zv7dxJyxmhYcTFEM9YFOeT'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


# In[126]:


hashtag_list = []

def hashtags_from_tweets(s):
    hashtag_list.clear()
    for i in s:
        hashtag_list.extend(word for word in i.split() if word.startswith('#'))
    return hashtag_list


# In[127]:


def most_common_hashtags(t):
    for x in t:
        top_five_hashtags = Counter(t).most_common(5)
    return top_five_hashtags


# In[128]:


def tweets_from_coordinates(x, y):
    tweet_geocode = str(x) + "," + str(y) + ",1km"
    return api.search(geocode=tweet_geocode, count = 1000, tweet_mode = 'extended')


# In[129]:


geolocator = Nominatim(user_agent = "trendy")

def coordinates_from_location(x):
    location = geolocator.geocode(x)
    return location.latitude, location.longitude
    


# In[130]:


print(coordinates_from_location("New York"))


# In[131]:


tweets_test = tweets_from_coordinates(coordinates_from_location("Edinburgh")[0],coordinates_from_location("Edinburgh")[1])


# In[119]:


tweet_text_list = []

def tweets_text_list(x):
    tweet_text_list.clear()
    for i in x:
        tweet_text_list.append(str(i.full_text))
    return tweet_text_list


# In[121]:


hashtags_from_tweets(tweets_text_list(tweets_from_coordinates(40.7127281, -74.0060152)))
print(hashtag_list)


# In[39]:


print(most_common_hashtags(hashtag_list))


# In[40]:


tweet_testing_example = ['#Edinburgh', '#UnitedKingdom', '#foodwaste', '#free', '#Edinburgh', '#Sales', '#statistics',
                         '#Edinburgh', '#Edinburgh.', '#Healthcare', '#Edinburgh!', '#Healthcare', '#statistics',
                         '#Edinburgh', '#Edinburgh', '#UnitedKingdom', '#foodwaste', '#free', '#Edinburgh', '#UnitedKingdom',
                         '#foodwaste', '#free', '#Edinburgh', '#UnitedKingdom', '#foodwaste', '#free', '#Edinburgh',
                         '#UnitedKingdom', '#foodwaste', '#free', '#Retail', '#GeneralScience', '#statistics', '#Healthcare',
                         '#Edinburgh', '#Sales', '#Edinburgh', '#Edinburgh?', '#Healthcare', '#statistics', '#Edinburgh',
                         '#clinical', '#Edinburgh', '#Retail', '#statistics', '#Edinburgh', '#smallbusinessowner',
                         '#smallbusinessuk', '#glutenfreefood', '#foodlover😍', '#glutenfreefood', '#onlineorders',
                         '#Edinburgh.', '#clinical', '#SCOIRE', '#statistics', '#Edinburgh', '#smallbusinessowner',
                         '#mothersday', '#glutenfreefoods', '#foodlovers', '#Retail', '#ClassicOrganicCotton', '#fachadas',
                         '#edimburgueando', '#statistics', '#Edinburgh', '#descansodominical', '#Edinburgh', '#UnitedKingdom',
                         '#foodwaste', '#free', '#Edinburgh', '#UnitedKingdom', '#foodwaste', '#free', '#sayhername',
                         '#saraheverard', '#reclaimthenight', '#reclaimthestreets', '#Edinburgh', '#UnitedKingdom',
                         '#foodwaste', '#free', '#ReclaimTheseStreets', '#LNER', '#oldedinburgh', '#edinburgholdtown',
                         '#caltonhill', '#edinphoto', '#foreveredinburgh', '#artdeco', '#Edinburgh.', '#Sales', '#Edinburgh',
                         '#UnitedKingdom', '#foodwaste', '#free', '#live', '#naptime😴', '#Retail', '#weekendtime',
                         '#sobremesa', '#lockdown', '#19crimeswine', '#saturdaymood', '#seeingusthroughlockdown', '#weekend',
                         '#statistics', '#Edinburgh', '#Edinburgh', '#UnitedKingdom', '#foodwaste', '#free', '#Edinburgh,',
                         '#Healthcare', '#InstaPlaces', '#InstaMomments', '#InstaFollow', '#InstaPic', '#InstaPics',
                         '#InstaPicture', '#InstaPictures', '#InstaPhoto', '#InstaPhotos', '#InstaTravel', '#ReinoUnido',
                         '#UnitedKingdom', '#Escocia', '#Scotland', '#Edinburgh', '#UnitedKingdom', '#zerowaste', '#free',
                         '#Edinburgh', '#UnitedKingdom', '#foodwaste', '#free', '#SkilledTrade', '#Edinburgh,', '#Edinburgh',
                         '#UnitedKingdom', '#zerowaste', '#free']


# In[42]:


top_five_edinburgh_hashtags = most_common_hashtags(tweet_testing_example)
print(top_five_edinburgh_hashtags)


# In[104]:


def hashtag_percentages(x):
    total_tweets = 0
    top_hashtag_percentages = []
    for i in x:
        total_tweets += i[1]
    for i in x:
        top_hashtag_percentages.extend((i[0],(round(i[1]/total_tweets,4)*100)))
    return top_hashtag_percentages


# In[105]:


print(hashtag_percentages(top_five_edinburgh_hashtags))


# In[98]:


print(top_five_edinburgh_hashtags[0][1])


# In[134]:


def top_five_hashtags(location = 'Default', x = 'Default', y = 'Default'):
    if location == 'Default':
        coord_hashtags = most_common_hashtags(hashtags_from_tweets(tweets_text_list(tweets_from_coordinates(x, y))))
        percent_hashtags = hashtag_percentages(coord_hashtags)
        return coord_hashtags, percent_hashtags
    elif x == 'Default' or y == 'Default':
        x = coordinates_from_location(location)[0]
        y = coordinates_from_location(location)[1]
        coord_hashtags = most_common_hashtags(hashtags_from_tweets(tweets_text_list(tweets_from_coordinates(x, y))))
        percent_hashtags = hashtag_percentages(coord_hashtags)
        return coord_hashtags, percent_hashtags


# In[135]:


print(top_five_hashtags(x = 40.7127281,y = -74.0060152))


# In[136]:


print(top_five_hashtags(location = "New York"))


# In[ ]:




