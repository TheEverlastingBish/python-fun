import pandas as pd

import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from twitterapiconn import *

import json
import csv


def convert_tweet_to_pd(jsonTweet):
	tweeDict = {}

	tweeDict['userName'] = jsonTweet["user"]["name"]
	tweeDict['tweetTimeStamp'] = jsonTweet["created_at"]
	tweeDict['tweetId'] = jsonTweet["id"]
	tweeDict['tweetText'] = jsonTweet["text"]
	
	return pd.DataFrame([tweeDict])


auth = OAuthHandler(cKey, cSecret)
auth.set_access_token(aToken, aSecret)
api = tweepy.API(auth)
print("Authenticated!")

tweeTarget = "NetworkResearch"
tweeCols = ['userName', 'tweetId' , 'tweetTimeStamp', 'tweetText']
tweeData = pd.DataFrame(columns=tweeCols)

for tweet in tweepy.Cursor(api.user_timeline, id = tweeTarget).items(100):
	temppd = convert_tweet_to_pd(tweet._json)
	tweeData = tweeData.append(temppd, ignore_index = True, columns = tweeCols)

fname = tweeTarget + "_Timeline.csv"
tweeData.to_csv(fname, sep = ",", encoding = "utf-8", mode="w", index=False, columns = tweeCols)
