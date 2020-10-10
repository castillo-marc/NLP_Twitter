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


query = "Tesla OR Elon"
tweets = tweepy.Cursor(api.search, q=query,
                       tweet_mode="extended",
                       date_since = "2020-09-01",
                       lang="en").items()

def tweet_text(tweet):
    if hasattr(tweet, "retweeted_status"):
        return tweet.retweeted_status.full_text
    return tweet.full_text

data = [[tweet.id_str,
          tweet.created_at,
          tweet.favorite_count,
          tweet.retweet_count,
          tweet.user.screen_name, 
          tweet.user.followers_count,
          tweet.source,
          tweet_text(tweet)] for tweet in tweets]

columns = ["id",
            "date_time",
            "likes", 
            "retweets", 
            "user", 
            "user_followers",
            "source",
            "body"]

tweet_df = pd.DataFrame(data=data, columns=columns)
pd.to_datetime(tweet_df["date_time"]).describe()
