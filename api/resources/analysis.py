"""A module defining Analysis resource.

Author: Teekayu Klongtruajrok
"""
from flask_restful import Resource, reqparse


class Analysis(Resource):
    """Analysis resource to perform sentiment analysis."""

    def __init__(self):
        """Initialize argument parsers."""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('query_phrase', type=str, help='Query phrase invalid.')

    def get(self):
        """GET Method retrieving sentiment analysis of a query phrase."""
        args = self.parser.parse_args()
        query_phrase = args['query_phrase']
        return query_phrase
