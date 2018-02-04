from flask_restful import Resource


class Analysis(Resource):

    def get(self):
        return {'hello': 'world'}
