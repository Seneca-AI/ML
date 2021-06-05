"""Cloud function definitions.  All functions simply forward to server.py"""
from flask import Flask, request

from . import server as app_server

app = Flask(__name__)

server = app_server.Server(False)

@app.route('/heartbeat', methods=['GET'])
def handle_heartbeat_request():
    """
    handle_heartbeat_request immediately response with 200 OK
    """
    print("Received request at /heartbeat")
    return server.handle_heartbeat_request(request)

@app.route('/lane_changing', methods=['POST'])
def handle_lane_changing_request():
    """
    handle_lane_changing_request is the entry point for
    lane_changing processing requests into the application.
    """
    print("Received request at /lane_changing")
    return server.handle_lane_changing_request(request)

@app.route('/following_distance', methods=['POST'])
def handle_following_distance_request():
    """
    handle_following_distance_request is the entry point for
    following_distance processing requests into the application.
    """
    print("Received request at /following_distance")
    return server.handle_following_distance_request(request)

@app.route('/objects_in_frame', methods=['POST'])
def handle_objects_in_frame_request():
    """
    handle_objects_in_frame_request is the entry point for
    objection_detection processing requests into the application..
    """
    print("Received request at /objects_in_frame")
    return server.handle_objects_in_frame_request(request)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
