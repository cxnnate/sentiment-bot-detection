import re
import string
import preprocessor as p
from nltk import word_tokens


class Tweet(Object):

    def __init__(self, created_at, tweet_id, text, hashtags, user_id, cleaned_tweet=""):

        self.created_at = created_at
        self.tweet_id = tweet_id
        self.text_ = text
        self.cleaned_tweet = cleaned_tweet
        self.user_id = user_id
        self._sentiment = 0
        self._bot = False
    
    def clean_tweet(self, text=None):
        # emoji_pattern + re.compile
        if text is None:
            text = self.text_
        
        tweet = p.clean(text)
        tweet = re.sub(r':', '', tweet)
        return tweet