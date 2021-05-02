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
        valid_output_path = "tests/data/raw_frames/out"

        with self.assertRaises(FileNotFoundError):
            generate_lane_masks(invalid_path, valid_output_path)


def test_does_not_crash():
    # Do not run in CI env.
    if os.getenv("CI"):
        return

    input_path = "tests/data/raw_frames/in"
    output_path = "tests/data/raw_frames/out/generate_lane_mask"
    os.mkdir(output_path)

    try:
        generate_lane_masks(input_path, output_path)
    except:
        shutil.rmtree(output_path)
        raise

    shutil.rmtree(output_path)
