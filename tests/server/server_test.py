"""
server_test tests all of the code in ml/server
"""

import unittest
from unittest.mock import patch

from pathlib import Path
import requests

from api.type import processed_pb2
from ml.server.server import Server

class TestServer(unittest.TestCase):

    @patch('ml.server.server.CloudStorageClient')
    def test_invalid_request_lane_changing(self, mock_gcsc):
        mock_gcsc.return_value = None
        mock_gcsc.download_file.return_value = "file"

        test_server = Server(True)

        request = requests.request("POST", "http://doesntmatter.com")

        # Test empty request.
        request.data = ""
        response = test_server.handle_lane_changing_request(request)
        self.assertEqual(response.status_code, 400)

        # Test request without request ID.
        lane_changes_for_video_request = processed_pb2.LaneChangesForVideoRequest()
        request.data = lane_changes_for_video_request.SerializeToString()
        response = test_server.handle_lane_changing_request(request)
        self.assertEqual(response.status_code, 400)

        # Test request without video URL.
        lane_changes_for_video_request.request_id = "123"
        request.data = lane_changes_for_video_request.SerializeToString()
        response = test_server.handle_lane_changing_request(request)
        self.assertEqual(response.status_code, 400)

        # Test request with invalid URL.
        lane_changes_for_video_request.simple_storage_video_url = "http://invalid"
        request.data = lane_changes_for_video_request.SerializeToString()
        response = test_server.handle_lane_changing_request(request)
        self.assertEqual(response.status_code, 400)

        # Test with exception thrown.
        mock_gcsc.download_file.side_effect = Exception()
        lane_changes_for_video_request.simple_storage_video_url = "gs://doesntmatter"
        request.data = lane_changes_for_video_request.SerializeToString()
        response = test_server.handle_lane_changing_request(request)
        self.assertEqual(response.status_code, 500)

    @patch('ml.server.server.CloudStorageClient.download_file')
    @patch('ml.server.server.CloudStorageClient.__init__')
    def test_returns_lane_changing_response(self, mock_gcsc_init, mock_download_file):
        mock_gcsc_init.return_value = None
        filepath = "tests/data/raw_videos/out/test_returns_lane_changing_response.mp4"
        mock_download_file.return_value = filepath

        # Create a random file for os.remove
        Path(filepath).touch()

        test_server = Server(True)

        lane_changes_for_video_request = processed_pb2.LaneChangesForVideoRequest()
        lane_changes_for_video_request.request_id = "123"
        lane_changes_for_video_request.simple_storage_video_url = "gs://doesntmatter"
        request = requests.request("POST", "http://doesntmatter.com")
        request.data = lane_changes_for_video_request.SerializeToString()

        lane_changes_for_video_response = processed_pb2.LaneChangesForVideoResponse()

        response = test_server.handle_lane_changing_request(request)
        self.assertEqual(response.status_code, 200)
        lane_changes_for_video_response.ParseFromString(response.response[0])
        self.assertEqual(
            lane_changes_for_video_response.request_id,
            lane_changes_for_video_request.request_id
            )
        self.assertGreater(
            len(lane_changes_for_video_response
                    .lane_changes_for_video.lane_change_for_frame),
            1)

    @patch('ml.server.server.CloudStorageClient')
    def test_invalid_request_following_distance(self, mock_gcsc):
        mock_gcsc.return_value = None
        mock_gcsc.download_file.return_value = "file"

        test_server = Server(True)

        request = requests.request("POST", "http://doesntmatter.com")

        # Test empty request.
        request.data = ""
        response = test_server.handle_following_distance_request(request)
        self.assertEqual(response.status_code, 400)

        # Test request without request ID.
        following_distances_for_video_request = processed_pb2.FollowingDistanceForVideoRequest()
        request.data = following_distances_for_video_request.SerializeToString()
        response = test_server.handle_following_distance_request(request)
        self.assertEqual(response.status_code, 400)

        # Test request without video URL.
        following_distances_for_video_request.request_id = "123"
        request.data = following_distances_for_video_request.SerializeToString()
        response = test_server.handle_following_distance_request(request)
        self.assertEqual(response.status_code, 400)

        # Test request with invalid URL.
        following_distances_for_video_request.simple_storage_video_url = "http://invalid"
        request.data = following_distances_for_video_request.SerializeToString()
        response = test_server.handle_following_distance_request(request)
        self.assertEqual(response.status_code, 400)

        # Test with exception thrown.
        mock_gcsc.download_file.side_effect = Exception()
        following_distances_for_video_request.simple_storage_video_url = "gs://doesntmatter"
        request.data = following_distances_for_video_request.SerializeToString()
        response = test_server.handle_following_distance_request(request)
        self.assertEqual(response.status_code, 500)

    @patch('ml.server.server.CloudStorageClient.download_file')
    @patch('ml.server.server.CloudStorageClient.__init__')
    def test_returns_following_distance_response(self, mock_gcsc_init, mock_download_file):
        mock_gcsc_init.return_value = None
        filepath = "tests/data/raw_videos/out/test_returns_following_distance_response.mp4"
        mock_download_file.return_value = filepath

        # Create a random file for os.remove
        Path(filepath).touch()

        test_server = Server(True)

        following_distances_for_video_request = processed_pb2.FollowingDistanceForVideoRequest()
        following_distances_for_video_request.request_id = "123"
        following_distances_for_video_request.simple_storage_video_url = "gs://doesntmatter"
        request = requests.request("POST", "http://doesntmatter.com")
        request.data = following_distances_for_video_request.SerializeToString()

        following_distances_for_video_response = processed_pb2.FollowingDistanceForVideoResponse()

        response = test_server.handle_following_distance_request(request)
        self.assertEqual(response.status_code, 200)
        following_distances_for_video_response.ParseFromString(response.response[0])
        self.assertEqual(
            following_distances_for_video_response.request_id,
            following_distances_for_video_request.request_id
            )
        self.assertGreater(
            len(following_distances_for_video_response
                    .following_distance_for_video.following_distance_for_frame),
            1)
