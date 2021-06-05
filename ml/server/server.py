"""Server is the shared logic for Flask and Google Cloud Functions."""
import os

from flask import Response
import requests

from api.type import processed_pb2
from api import constants
from ml.cloud.google.cloud_storage import CloudStorageClient
from ml.runners.following_distance import mark_following_distance
from ml.runners.lane_changing import get_lane_changes_for_video
from ml.runners.object_detection import ObjectDetector

class Server:
    """
    Server handles incoming requests.
    """

    def __init__(self, unit_test_mode: bool):
        self.gcs_client = CloudStorageClient()
        if not unit_test_mode:
            self.object_detector = ObjectDetector(
                constants.PATH_TO_OBJECT_DETECTION_CONFIG,
                constants.PATH_TO_OBJECT_DETECTION_WEIGHTS,
                )
        self.unit_test_mode = unit_test_mode

    # pylint: disable=unused-argument,no-self-use
    def handle_heartbeat_request(self, request: requests.request) -> Response:
        """
        handle_heartbeat_request immediately response with 200 OK
        Params:
            request requests.request
        Returns:
            flask.Response
        """
        return Response(status=200, response="ok")

    def handle_lane_changing_request(self, request: requests.request) -> Response:
        """
        handle_lane_changing_request is the entry point for
        lane_changing processing requests into the application.
        Params:
            request requests.request: a requests request where request.data
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
            get_lane_changes_for_video(path_to_video_file))

        os.remove(path_to_video_file)

        return Response(status=200, response=self.stringify_response(lane_changing_response))

    def handle_following_distance_request(self, request: requests.request) -> Response:
        """
        handle_following_distance_request is the entry point for
        following_distance processing requests into the application.
        Params:
            request requests.request: a requests request where request.data
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

    def handle_objects_in_video_request(self, request: requests.request) -> Response:
        """
        handle_objects_in_video_request is the entry point for
        objects_in_video processing requests into the application.
        Params:
            request requests.request: a requests request where request.data
                    must deserialize to a ObjectsInVideoRequest
        Returns:
            flask.Response: flask.Response(
                response=str(api.type.ObjectsInVideoResponse )...)
        """
        objects_in_video_request_data = request.data
        objects_in_video_request = processed_pb2.ObjectsInVideoRequest()
        try:
            objects_in_video_request.ParseFromString(objects_in_video_request_data)
        except: # pylint: disable=bare-except
            return Response(status=400, response="Malformed request data.")

        # TODO(lucaloncar): figure out a better way to enforce type here
        if objects_in_video_request.request_id == '':
            return Response(status=400, response="Missing request_id field.")
        if objects_in_video_request.simple_storage_video_url == '':
            return Response(status=400, response="Missing simple_storage_video_url field.")
        if not objects_in_video_request.simple_storage_video_url.startswith('gs://'):
            return Response(status=400, response="File URL must begin with 'gs://")

        try:
            path_to_video_file = self.gcs_client.download_file(
                objects_in_video_request.simple_storage_video_url)
        except: # pylint: disable=bare-except
            # TODO(lucaloncar): return 400 if file does not exist
            return Response(
                status=500, response="Error downloading video file from GoogleCloudStorage.")

        objects_in_frames = self.object_detector.classify_video(path_to_video_file)

        objects_in_video_response = processed_pb2.ObjectsInVideoResponse()
        objects_in_video_response.request_id = objects_in_video_request.request_id
        for frame_index, frame in objects_in_frames.items():
            objects_in_frame_numbered = processed_pb2.ObjectsInVideoResponse.ObjectsInFrameNumbered(
            )
            objects_in_frame_numbered.frame_index = frame_index
            print(frame)
            objects_in_frame_numbered.object_in_frame.CopyFrom(frame)
            objects_in_video_response.objects_in_frame_numbered.append(objects_in_frame_numbered)

        os.remove(path_to_video_file)

        return Response(status=200, response=self.stringify_response(objects_in_video_response))


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
