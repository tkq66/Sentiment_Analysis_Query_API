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
            A dict of list of text data, grouped by sentiment categories.
            Formatting as follows:
                {
                    '1': [
                        {
                            'id': <tweet id>,
                            'text': <tweet text>,
                            'user': <twitter user id>,
                            'timestamp': <tweeted date>,
                            'polarity': <tweet sentiment>
                        }
                        ...
                    ],
                    '0': ...
                    '-1': ...
                }

        """
        args = self.parser.parse_args()
        query_phrase = args['query_phrase']
        data_list = analysis_business_logic.construct_data_source(query_phrase)
        data_grouping = analysis_business_logic.group_text_by_sentiment(data_list)
        return data_grouping
