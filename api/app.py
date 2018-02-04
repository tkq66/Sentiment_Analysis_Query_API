from flask import Flask
from flask_restful import Api
from .resources import Analysis

app = Flask(__name__)
api = Api(app)

api.add_resource(Analysis, '/', '/Analysis')
