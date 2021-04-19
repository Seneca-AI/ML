"""Cloud function definitions.  All functions simply forward to server.py"""
from ml.server import server

def lane_changing(request):
    """
    lane_changing is the entry point for
    processing lane_changing requests into the application
    when deployed to cloud.
    """
    return server.handle_lane_changing_request(request)

def following_distance(request):
    """
    following_distance is the entry point for processing
    following_distance requests into the application
    when deployed to cloud.
    """
    return server.handle_following_distance_request(request)
