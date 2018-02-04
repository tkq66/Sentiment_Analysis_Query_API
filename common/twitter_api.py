"""A module providing Twitter API object.

Author: Teekayu Klongtruajrok
"""
from config import BaseConfig as config
import twitter


twitter_api = twitter.Api(consumer_key=config.TWITTER['consumer_key'],
                          consumer_secret=config.TWITTER['consumer_secret'],
                          access_token_key=config.TWITTER['access_token_key'],
                          access_token_secret=config.TWITTER['access_token_secret'])
