"""A module defining core Flask app and routes.

Author: Teekayu Klongtruajrok
"""
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from .resources import Analysis

app = Flask(__name__)
cors = CORS(app, resources={"/api/*": {"origins": "*"}})
api = Api(app)

api.add_resource(Analysis, '/api/Analysis')
