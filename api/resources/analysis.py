"""A module defining Analysis resource.

Author: Teekayu Klongtruajrok
"""
import re
from common import twitter_api
from flask_restful import Resource, reqparse
from urllib.parse import quote_plus
from textblob import TextBlob


class Analysis(Resource):
    """Analysis resource to perform sentiment analysis."""

    def __init__(self):
        """Initialize argument parsers and query parameters."""
        # Arg parsers
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('query_phrase',
                                 type=str,
                                 help='Query phrase invalid.')
        # Query parameters
        self.query_count = 5
        self.tweet_mode = 'extended'
        self.filter_query = ' AND '.join([
            '-filter:retweets',
            '-filter:replies',
            '-filter:links',
            '-filter:media'
        ])

    def get(self):
        """GET Method retrieving sentiment analysis of a query phrase."""
        args = self.parser.parse_args()
        query_phrase = args['query_phrase']
        raw_query = 'q={}{}&count={}&tweet_mode={}'.format(query_phrase,
                                                           self.filter_query,
                                                           self.query_count,
                                                           self.tweet_mode)
        encoded_query = quote_plus(raw_query, safe="&=")
        query_results = twitter_api.GetSearch(raw_query=encoded_query)
        local_result = [self.__map_tweets_to_local(result) for result in query_results]
        return local_result

    def __map_tweets_to_local(self, tweet_status):
        """Map twitter.Status object to relevant dict.

        Args:
            tweet_status: A twitter.Status object storing tweet data.

        Returns:
            A dict of minimal tweet info. Formatting as follows:
                {
                    'id': <tweet id>,
                    'text': <tweet text>,
                    'user': <twitter user id>,
                    'timestamp': <tweeted date>
                }

        """
        return {
            'id': tweet_status.id_str,
            'text': tweet_status.full_text,
            'user': tweet_status.user.screen_name,
            'timestamp': tweet_status.created_at
        }

    def __clean_tweet(self, tweet):
        """Clean tweet text by removing links, special characters.

        Args:
            tweet: A string of raw tweet data.

        Returns:
            A string of cleaned-up tweet.

        """
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
