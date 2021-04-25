"""Server is the shared logic for Flask and Google Cloud Functions."""
import os

from flask import Response
import requests

from api.type import processed_pb2
from ml.cloud.google.cloud_storage import CloudStorageClient
from ml.runners.lane_changing import mark_lane_changes
from ml.runners.following_distance import mark_following_distance


class Server:
    """
    Server handles incoming requests.
    """

    def __init__(self, unit_test_mode: bool):
        self.gcs_client = CloudStorageClient()
        self.unit_test_mode = unit_test_mode

    def handle_lane_changing_request(self, request: requests.request) -> Response:
        """
        handle_lane_changing_request is the entry point for
        lane_changing processing requests into the application.
        Params:
            request requests.request: an requests request where request.data
                    must deserialize to a LaneChangesForVideoRequest
        Returns:
            flask.Response: flask.Response(response=str(api.type.LaneChangesForVideoResponse)...)
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
        if not lane_changing_request.simple_storage_video_url.startswith('gs://'):
            return Response(status=400, response="File URL must begin with 'gs://")

        try:
            path_to_video_file = self.gcs_client.download_file(
                lane_changing_request.simple_storage_video_url)
        except: # pylint: disable=bare-except
            # TODO(lucaloncar): return 400 if file does not exist
            return Response(
                status=500, response="Error downloading video file from GoogleCloudStorage.")

        lane_changing_response = processed_pb2.LaneChangesForVideoResponse()
        lane_changing_response.request_id = lane_changing_request.request_id
        lane_changing_response.lane_changes_for_video.CopyFrom(
            mark_lane_changes(path_to_video_file))

        os.remove(path_to_video_file)

        return Response(status=200, response=self.stringify_response(lane_changing_response))

    def handle_following_distance_request(self, request: requests.request) -> Response:
        """
        handle_following_distance_request is the entry point for
        following_distance processing requests into the application.
        Params:
            request requests.request: an requests request where request.data
                    must deserialize to a FollowingDistanceForVideoRequest
        Returns:
            flask.Response: flask.Response(
                response=str(api.type.FollowingDistanceForVideoResponse)...)
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
        if not following_distance_request.simple_storage_video_url.startswith('gs://'):
            return Response(status=400, response="File URL must begin with 'gs://")

        try:
            path_to_video_file = self.gcs_client.download_file(
                following_distance_request.simple_storage_video_url)
        except: # pylint: disable=bare-except
            # TODO(lucaloncar): return 400 if file does not exist
            return Response(
                status=500, response="Error downloading video file from GoogleCloudStorage.")

        following_distance_response = processed_pb2.FollowingDistanceForVideoResponse()
        following_distance_response.request_id = following_distance_request.request_id
        following_distance_response.following_distance_for_video.CopyFrom(
            mark_following_distance(path_to_video_file))

        os.remove(path_to_video_file)

        return Response(status=200, response=self.stringify_response(following_distance_response))

    def stringify_response(self, response) -> str:
        """
        stringify_response decies whether to call str(response) or
        response.SerializeToString() based on whether or not the server is
        in unit test mode.

        Params:
            response [LaneChanges | FolliwingDistance]ForVideoResponse: the response to stringify
        Returns:
            string
        """
        if self.unit_test_mode:
            return response.SerializeToString()
        return str(response)
