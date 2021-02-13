import os
import sys
import csv
import json
import time
import datetime
import argparse
import tweepy
from tweet import Tweet

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class CustomStreamListener(tweepy.StreamListener):
    """
    A custom stream listener object for Tweepy to use for streaming Twitter data
    """
    def __init__(self, time_limit): #), tweet_file, user_file):
        """
        :return: A Twepy Stream Listener
        """
    
        super(CustomStreamListener, self).__init__()
        self.start_time = time.time()
        self.time_limit = time_limit
        self.tweet_file = open(ROOT + '/twitter/data/streamed_tweets_' + str(datetime.date.today()) + '.csv', 'w+')
        self.user_file = open(ROOT + '/twitter/data/streamed_users_' + str(datetime.date.today()) + '.csv', 'w+')

    
    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False


    def on_status(self, status):
        """
        Processes the data from the Tweepy stream
        :param raw_data: Raw data from stream 
        :return: None
        """
        print(type(status[0]))
        response = json.dumps(status._json)
        
    
        # print(type(response))
     
    #     write_tweets = csv.writer(self.tweet_file, quoting=csv.QUOTE_NONNUMERIC, delimiter=',', lineterminator='\n')
    #     write_users = csv.writer(self.user_file, quoting=csv.QUOTE_NONNUMERIC, delimiter=',', lineterminator='\n')

    # #     if (time.time() - self.start_time) < self.time_limit:

    #     if 'extended_tweet' in response:
    #         response['text'] = response['extended_tweet']['full_text']

    #     if 'entities' in response:
    #         hashtags = [hashtag['text'] for hashtag in response['id_str'], response['text']]

    #     if 'limit' in response:
    #         pass
    #     else:
    #         tweet = Tweet(response['created_at'], response['id_str'], response['text'], 
    #                         hashtags, response['user']['id'])
    #         tweet.clean_tweet()
    #         print("tweet: ", tweet.cleaned_tweet)
    #             write_tweets.writerow((tweet.created_at, tweet.tweet_id, tweet.text_, tweet.cleaned_tweet,
    #                                    tweet.hashtags_, tweet.user_id))
                
    #             write_users.writerow((data['user']))
    # # def 


if __name__ == '__main__':

    with open(ROOT + '/twitter/data/cred.json', 'r') as f:
        creds = json.load(f)

    auth = tweepy.OAuthHandler(creds['twitter_consumer_key'], creds['twitter_consumer_secret'])
    auth.set_access_token(creds['twitter_access_key'], creds['twitter_access_secret'])
    api = tweepy.API(auth)

    time_limit = 60
    keywords = ['Donald', 'Trump', 'Impeachment', 'President', 'Biden']

    stream = tweepy.Stream(auth=api.auth, listener=CustomStreamListener(time_limit=time_limit))
    print(stream)
    stream.filter(track=keywords, languages=['en'])
    
    # print(creds)