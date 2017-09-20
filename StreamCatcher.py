from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from twitterapistuff import *
import pandas as pd

class listener(StreamListener):

	def on_status(self, status):
	
		tweeDict = {}

		tweeDict['userName'] = status.user.screen_name
		tweeDict['userDisplayName'] = status.user.name
		tweeDict['userDescription'] = status.user.description
		tweeDict['userLocation'] = status.user.location
		tweeDict['userFollowers'] = status.user.followers_count
		tweeDict['tweetTimeStamp'] = status.created_at
		tweeDict['tweetTimeStamp_ms'] = int(status.timestamp_ms)
		tweeDict['tweetId'] = status.id
		tweeDict['tweetText'] = status.text
		
		global tweeCols
		
		tweeTemp = pd.DataFrame([tweeDict])
		
		tweeTemp.to_csv(fname, sep = ",", encoding = "utf-8", mode="a", index=False, header = False, columns = tweeCols)

		return(True)
		
	def on_error(self, status):
		print(status)


auth = OAuthHandler(cKey, cSecret)
auth.set_access_token(aToken, aSecret)
print("Started streaming...")

tweeTrackers = ["Brexit", "brexit"]
tweeCols = ['userName' , 'userDisplayName' , 'userDescription' , 'userLocation' , 'userFollowers' , 'tweetTimeStamp' , 'tweetId' , 'tweetText']
tweeData = pd.DataFrame(columns=tweeCols)

fname = str(tweeTrackers[0]) + "_Mentions.csv"

initfile = open(fname, "w")
tweeData.to_csv(initfile, index = False)
initfile.close()

twitterStream = Stream(auth, listener())
twitterStream.filter(track=tweeTrackers)
