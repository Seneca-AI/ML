"""Cloud function definitions."""
from flask import Response

from api.type import processed_pb2

# TODO(lucaloncar): test these functions

def handle_lane_changing_request(request):
    """
    handle_lane_changing_request is the entry point for
    lane_changing processing requests into the application.
    Params:
        request http.request: an http request where request.data
                must deserialize to a LaneChangesForVideoRequest
    Returns:
        string: str(api.type.LaneChangesForVideoResponse)
    """
    lane_changing_request_data = request.data
    lane_changing_request = processed_pb2.LaneChangesForVideoRequest()
    try:
        lane_changing_request.ParseFromString(lane_changing_request_data)
    except: # pylint: disable=bare-except
        return Response(status=400, response="Malformed request data.")

    # TODO(lucaloncar): figure out a better way to enforce type here
    if lane_changing_request.request_id == '':
        return Response(status=400, response="Missing request_id field.")
    if lane_changing_request.simple_storage_video_url == '':
        return Response(status=400, response="Missing simple_storage_video_url field.")

    print("lane_changing_request: "+ str(lane_changing_request))
    lane_changing_response = processed_pb2.LaneChangesForVideoResponse()
    lane_changing_response.request_id = lane_changing_request.request_id
    lane_changing_response.lane_changes_for_video.num_frames = 5
    return Response(status=200, response=str(lane_changing_response))

def handle_following_distance_request(request):
    """
    handle_following_distance_request is the entry point for
    following_distance processing requests into the application.
    Params:
        request http.request: an http request where request.data
        must deserialize to a FollowingDistanceForVideoRequest
    Returns:
        string: str(api.type.FollowingDistanceForVideoResponse)
    """
    following_distance_request_data = request.data
    following_distance_request = processed_pb2.FollowingDistanceForVideoRequest()
    try:
        following_distance_request.ParseFromString(following_distance_request_data)
    except: # pylint: disable=bare-except
        return Response(status=400, response="Malformed request data.")

    # TODO(lucaloncar): figure out a better way to enforce type here
    if following_distance_request.request_id == '':
        return Response(status=400, response="Missing request_id field.")
    if following_distance_request.simple_storage_video_url == '':
        return Response(status=400, response="Missing simple_storage_video_url field.")

    print("following_distance_request: "+ str(following_distance_request))
    following_distance_response = processed_pb2.FollowingDistanceForVideoResponse()
    following_distance_response.request_id = following_distance_request.request_id
    # TODO(lucaloncar): fix this
    following_distance_response.lane_changes_for_video.num_frames = 10
    return str(following_distance_response)
