"""Cloud function definitions.  All functions simply forward to server.py"""
from flask import Flask, request

from . import server

app = Flask(__name__)

@app.route('/lane_changing', methods=['POST'])
def handle_lane_changing_request():
    """
    handle_lane_changing_request is the entry point for
    lane_changing processing requests into the application
    when testing locally in flask.
    """
    return server.handle_lane_changing_request(request)

@app.route('/following_distance', methods=['POST'])
def handle_following_distance_request():
    """
    handle_following_distance_request is the entry point for
    following_distance processing requests into the application
    when testing locally in flask.
    """
    return server.handle_following_distance_request(request)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
