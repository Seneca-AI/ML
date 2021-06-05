"""
object_detection_test tests object_detection.py
"""

import os
import unittest

from ml.runners.object_detection import ObjectDetector

class TestObjectDetection(unittest.TestCase):

    def test_has_expected_output_length(self):
         # Do not run in CI env.
        if os.getenv("CI"):
            return

        config_file_path = "config/ml_config/yolov4x-mish.cfg"
        weights_file_path = "config/ml_config/yolov4x-mish.weights"

        object_detector = ObjectDetector(config_file_path, weights_file_path)

        path_to_video = "tests/data/raw_videos/in/second.mp4"

        objects_in_frames = object_detector.classify_video(path_to_video)

        self.assertEqual(30, len(objects_in_frames))

        for _, frame in objects_in_frames.items():
            self.assertGreater(len(frame.object_box), 0)
