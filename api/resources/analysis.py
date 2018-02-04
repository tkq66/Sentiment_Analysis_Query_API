from flask_restful import Resource, reqparse


class Analysis(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('query_phrase', type=str, help='Query phrase invalid.')

    def get(self):
        args = self.parser.parse_args()
        query_phrase = args['query_phrase']
        return query_phrase
