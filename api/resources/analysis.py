"""A module defining Analysis resource.

Author: Teekayu Klongtruajrok
"""
from .business_logic import analysis_business_logic
from flask_restful import Resource, reqparse


class Analysis(Resource):
    """Analysis resource to perform sentiment analysis."""

    def __init__(self):
        """Initialize argument parsers."""
        # Arg parsers
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('query_phrase',
                                 type=str,
                                 help='Query phrase invalid.')

    def get(self):
        """GET Method retrieving sentiment analysis of a query phrase.

        Args:
            query_phrase: A string of phrase to search Tweets with.

        Returns:
            A list of text data. Formatting as follows:
                [
                    {
                        'id': <tweet id>,
                        'text': <tweet text>,
                        'user_handle': <twitter user id>,
                        'user_name': <twitter user name>,
                        'user_img_url': <user profile image url>
                        'timestamp': <tweeted date>,
                        'polarity': <tweet sentiment>
                    }
                    ...
                ]

        """
        args = self.parser.parse_args()
        query_phrase = args['query_phrase']
        print('Querying...')
        data_list = analysis_business_logic.construct_data_source(query_phrase)
        print('Querying successful: {} tweets'.format(len(data_list)))
        return data_list
