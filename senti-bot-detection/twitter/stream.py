import os
import re
import sys
import csv
import json
import time
import datetime
import argparse
import tweepy

import pprint
from tweet import Tweet
import preprocessor.api as p
from preprocessor.api import clean, tokenize, parse


pp = pprint.PrettyPrinter(indent=4)
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
        self.tweet_file = open(ROOT + '/twitter/data/streamed_tweets_' + str(datetime.date.today()) + '.csv', 'a+')
        self.user_file = open(ROOT + '/twitter/data/streamed_users_' + str(datetime.date.today()) + '.csv', 'a+')

    
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
        if status is not None:
            print(status.text)
            return True
        else:
            raise Exception


    def on_data(self, tweet):
        """
        Processes the data from the Tweepy stream
        :param raw_data: Raw data from stream 
        :return: None
        """
        hashtags = []
        response = json.loads(tweet)
        

        write_tweets = csv.writer(self.tweet_file, quoting=csv.QUOTE_NONNUMERIC, delimiter=',', lineterminator='\n')
        write_users = csv.writer(self.user_file, quoting=csv.QUOTE_NONNUMERIC, delimiter=',', lineterminator='\n')

        if (time.time() - self.start_time) < self.time_limit:
            if 'text' in response: print(response['text'])

            if 'extended_tweet' in response:
                response['text'] = response['extended_tweet']['full_text']

            if 'entities' in response:
                if not response['entities']['hashtags']:
                    hashtags = []
                else:
                    hashtags = [hashtag['text'] for hashtag in response['entities']['hashtags']]
            
            if 'limit' in response:
                pass
            else:
                write_tweets.writerow((response['created_at'], response['id'],response['text'], self.clean(response['text']),
                                    hashtags, response['user']['id']))
                write_users.writerow((response['user']['id'], response['user']['screen_name'],
                                    response['user']['followers_count'], response['user']['friends_count'],
                                    response['user']['statuses_count'], response['user']['created_at']))
            return True

        else:
            self.tweet_file.close()
            self.user_file.close()
            return False
    
    def clean(self, text):
        """
        Parses and cleans a tweet
        :param: Text of the tweet
        :return: A cleaned tweet
        """
        if text is None:
            text = self.text_

        tweet = p.clean(text)
        tweet = re.sub(r':', '', tweet)

        return tweet


def parse_cli():
    """
    Reads from command-line arguments
    :return: args
    """

    parser = argparse.ArgumentParser(description='Streamer settings')
    parser.add_argument('--creds', type=str, help='Twitter API Credentials file')
    parser.add_argument('--keys', type=str, help='List of keywords to track on Twitter')
    parser.add_argument('--time', type=int, help='Time to stream Twitter')

    return parser.parse_args()


def main(args):
    """
    Run streamer
    """
    if args.creds is not None:
        with open(ROOT + '/twitter/' + args.creds, 'r') as f:
            creds = json.load(f)
    else:
        print('Invalid API credentials file')
        sys.exit(0)

    if args.keys is not None:
        with open(ROOT + '/twitter/' + args.keys, 'r') as f:
            keywords = f.read().splitlines()
    else:
        print('Invalid keyword file')
        sys.exit(0)

    time_limit = args.time

    auth = tweepy.OAuthHandler(creds['twitter_consumer_key'], creds['twitter_consumer_secret'])
    auth.set_access_token(creds['twitter_access_key'], creds['twitter_access_secret'])
    api = tweepy.API(auth)

    stream = tweepy.Stream(auth=api.auth, listener=CustomStreamListener(time_limit=time_limit))
    stream.filter(track=keywords, languages=['en'])
    

if __name__ == '__main__':
    main(parse_cli())
