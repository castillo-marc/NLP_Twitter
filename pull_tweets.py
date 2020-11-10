#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 20:06:23 2020

@author: marccastillo
"""

import os
import tweepy
# import GetOldTweets3 as got # doesn't work right now
import pandas as pd
from datetime import datetime

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_secret = os.environ.get("ACCESS_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)


# query = "Tesla OR Elon"
# tweets = tweepy.Cursor(api.search, q=query,
#                        tweet_mode="extended",
#                        date_since = "2020-09-01",
#                        lang="en").items()

# def tweet_text(tweet):
#     if hasattr(tweet, "retweeted_status"):
#         return tweet.retweeted_status.full_text
#     return tweet.full_text

# data = [[tweet.id_str,
#           tweet.created_at,
#           tweet.favorite_count,
#           tweet.retweet_count,
#           tweet.user.screen_name, 
#           tweet.user.followers_count,
#           tweet.source,
#           tweet_text(tweet)] for tweet in tweets]

# columns = ["id",
#             "date_time",
#             "likes", 
#             "retweets", 
#             "user", 
#             "user_followers",
#             "source",
#             "body"]

# tweet_df = pd.DataFrame(data=data, columns=columns)
# pd.to_datetime(tweet_df["date_time"]).describe()

# after tesla.txt is constructed:

tweet_url = pd.read_csv("tesla.txt", index_col=None, header=None, names=["links"])
af = lambda x: x["links"].split("/")[-1]
tweet_url["id"] = tweet_url.apply(af, axis=1)

ids = tweet_url["id"].tolist()

# still need to instantiate api 

# this function from:
# https://medium.com/@jcldinco/downloading-historical-tweets-using-tweet-ids-via-snscrape-and-tweepy-5f4ecbf19032
def fetch_tw(ids):
    list_of_tw_status = api.statuses_lookup(ids, tweet_mode= "extended")
    empty_data = pd.DataFrame()
    for status in list_of_tw_status:
            tweet_elem = {"id": status.id,
                     "user": status.user.screen_name,
                     "text":status.full_text,
                     "date_time":status.created_at}
            empty_data = empty_data.append(tweet_elem, ignore_index = True)
    empty_data.to_csv("tesla_tweets.csv", mode="a")
    
    
# process 50 entries at a time, bc original author couldn't loop through literally everything

total_count = len(ids)
chunks = (total_count - 1) // 50 + 1

for i in range(chunks):
    batch = ids[i*50:(i+1)*50]
    result = fetch_tw(batch)
    
