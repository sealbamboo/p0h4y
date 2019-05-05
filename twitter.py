from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, API, Cursor
from tweepy import Stream

import config

#  #  #  # TWITTER CLIENT #  #  #  #
class TwitterClient():
    def __init__(self, twiiter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twiiter_user

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

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

    
if __name__ == "__main__":

    # Authenticate using config.py and connect to Twitter Streaming API
    hash_tags_list = ['skin care','skincare','skin news','healthcare skin news']
    fetched_tweet_filename = './testData/tweets_bbc.json'

    twitter_client = TwitterClient('bbchealth')
    print(twitter_client.get_user_timeline_tweets(1))

    # twitter_streamer = TwitterStreamer()
    # twitter_streamer.stream_tweets(fetched_tweet_filename,hash_tags_list)