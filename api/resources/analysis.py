"""A module defining Analysis resource.

Author: Teekayu Klongtruajrok
"""
from flask_restful import Resource, reqparse
from common import twitter_api
from urllib.parse import quote_plus
import pprint

pp = pprint.PrettyPrinter(indent=4)


class Analysis(Resource):
    """Analysis resource to perform sentiment analysis."""

    def __init__(self):
        """Initialize argument parsers and query parameters."""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('query_phrase',
                                 type=str,
                                 help='Query phrase invalid.')

        self.query_count = 15
        self.tweet_mode = 'extended'
        filter_out_rt = '-filter:retweets'
        filter_out_reply = '-filter:replies'
        filter_out_link = '-filter:links'
        filter_out_media = '-filter:media'
        self.filter_query = ' {} AND {} AND {} AND {}'.format(filter_out_rt,
                                                              filter_out_reply,
                                                              filter_out_link,
                                                              filter_out_media)

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
        local_result = [self.__mapTweetsToLocal(result) for result in query_results]
        return local_result

    def __mapTweetsToLocal(self, tweet_status):
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
