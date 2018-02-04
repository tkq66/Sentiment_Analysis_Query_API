"""A script to start the Flask server.

Running this module will start up a Flask REST API server to perform
twitter-based sentiment analysis.

Author: Teekayu Klongtruajrok
"""
from api import app

if __name__ == '__main__':
    app.run(debug=True)
