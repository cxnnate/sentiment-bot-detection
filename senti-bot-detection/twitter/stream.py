import os
import csv
import json
import time
import datetime
import tweepy

class CustomStreamListener(tweepy.StreamListener):

    def __init__(self, time_limit, tweet_file, user_file):
        """
        """
        super(CustomStreamListener, self).int()
        self.start_time = time.time()
        self.time_limit = time_limit
        self.tweet_file = open('data/'+ tweet_file + str(datetime.date.today()) + '.csv')
        self.user_file = open('data/' + user_file + str(datetime.date.today()) + '.csv')


    def on_data(self, raw_data):
        tweet_writer = csv.writer(self.tweet_file, quoting=csv.QUOTE_NONNUMERIC, delimiter=',', lineterminator='\n')
        user_writer = csv.writer(self.user_file, quoting=csv.QUOTE_NONNUMERIC, delimiter=',', lineterminator='\n')

        if (time.time() - self.start_time) < self.time_limit:
            json_data = json.loads(raw_data)

            if 'extended_tweet' in json_data:
                json_data['text'] = json_data['extended_tweet']['full_text']