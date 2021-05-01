"""
lane_changing_utils_test tests all of the code in ml/utils/fileutils/video_utils
"""

import os
import shutil
import unittest

from ml.utils.mlutils.lane_changing import generate_lane_masks

class TestGenerateLaneMasks(unittest.TestCase):

    def test_invalid_input(self):
        # Do not run in CI env.
        if os.getenv("CI"):
            return

        invalid_path = "error/do/not/exist"
        valid_input_path = "tests/data/raw_frames/in"
        valid_output_path = "tests/data/raw_frames/out"

        with self.assertRaises(Exception):
            generate_lane_masks(invalid_path, valid_output_path)

        with self.assertRaises(Exception):
            generate_lane_masks(valid_input_path, invalid_path)

    # pylint: disable=no-self-use
    def test_does_not_crash(self):
        # Do not run in CI env.
        if os.getenv("CI"):
            return

        input_path = "tests/data/raw_frames/in"
        output_path = "tests/data/raw_frames/out/generate_lane_mask"
        os.mkdir(output_path)

        generate_lane_masks(input_path, output_path)

        shutil.rmtree(output_path)
