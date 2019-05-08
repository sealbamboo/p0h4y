from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, API, Cursor
from tweepy import Stream

from textblob import TextBlob

import re
import config
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#  #  #  # TWITTER CLIENT #  #  #  #
class TwitterClient():
    def __init__(self, twiiter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twiiter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets
    
    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self,num_tweets):
        home_timeline = []
        for tweet in Cursor(self.twitter_client.home, id=self.twitter_user).items(num_tweets):
            home_timeline.append(tweet)
        return home_timeline


#  #  #  # TWITTER AUTHENTICATER #  #  #  #
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
        auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

        return auth


#  #  #  # TWITTER STREAMER #  #  #  #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()


    def stream_tweets(self, fetched_tweet_filename, hash_tags_list):
        # This handle Twitter authentication and the connection to the twiiter Streaming API

        listener = TwitterListener(fetched_tweet_filename)        
        auth = self.twitter_authenticator.authenticate_twitter_app()
        steam = Stream(auth, listener)
        steam.filter(track=hash_tags_list)

#  #  #  # TWITTER STREAM LISTENER #  #  #  #
class TwitterListener(StreamListener):
    """
    Basic listener class that just prints received tweets to stdout
    """
    def __init__(self, fetched_tweet_filename):
        self.fetched_tweet_filename = fetched_tweet_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweet_filename, 'a') as f:
                f.write(data)
            return True
        except BaseException as e:
            print("Error on data : %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            # Returing False on data method in case rate limit occurs
            return False
        print(status)

class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
    """

    def clean_tweet(self, tweet):
        # Clean the special character within tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    
    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1


    def tweets_to_data_frame(self,tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets],columns=['tweets'])
        df['tweetid'] = np.array([tweet.id for tweet in tweets])        
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['author'] = np.array([tweet.author for tweet in tweets])
        df['geo'] = np.array([tweet.geo for tweet in tweets])
        df['like'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        
        return df


    
if __name__ == "__main__":

    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()
    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name="bbchealth",count=20)
    print(dir(tweets[0]))

    # Create dataframe contain return tweets
    df = tweet_analyzer.tweets_to_data_frame(tweets)
    print(df.head()) 

    # Get average length over all tweets.
    print(np.mean(df['retweets']))
    # Get the number or likes for the most liked tweets.
    print(np.max(df['retweets']))
    # Time Series
    # time_likes = pd.Series(data=df['like'].values, index=df['date'])
    # time_likes.plot(figsize=(16,4),label='like',legend=True)
    # time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
    # time_retweets.plot(figsize=(16,4),color='r',label='retweets',legend=True)
    # plt.show()
    # =============================================================
    df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])

    # Authenticate using config.py and connect to Twitter Streaming API
    # hash_tags_list = ['skin care','skincare','skin news','healthcare skin news']
    # fetched_tweet_filename = './testData/tweets_bbc.json'

    # twitter_client = TwitterClient('bbchealth')
    # print(twitter_client.get_user_timeline_tweets(1))

    # twitter_streamer = TwitterStreamer()
    # twitter_streamer.stream_tweets(fetched_tweet_filename,hash_tags_list)