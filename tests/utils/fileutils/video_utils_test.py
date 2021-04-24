"""
video_utils_test tests all of the code in ml/utils/fileutils/video_utils
"""
import os
import shutil
import unittest

from ml.utils.fileutils.video_utils import frames_to_vid, vid_to_frames
from api.exceptions import InvalidInputError

class TestFramesToVid(unittest.TestCase):

    def test_invalid_input(self):
        with self.assertRaises(InvalidInputError):
            frames_to_vid("even/if/it/did/exist/", "random")

        with self.assertRaises(InvalidInputError):
            frames_to_vid("even/if/it/did/exist/*", "random")

        with self.assertRaises(FileNotFoundError):
            frames_to_vid("does/not/exist", "random")

    def test_writes_output(self):
        path_to_frames = "tests/data/raw_frames/in"

        self.assertTrue(os.path.isdir(path_to_frames))

        path_to_output_video = "tests/data/raw_videos/out/TestFramesToVid.test_writes_output.mp4"
        frames_to_vid(path_to_frames, path_to_output_video)

        self.assertTrue(os.path.isfile(path_to_output_video))
        os.remove(path_to_output_video)

class TestVidToFrames(unittest.TestCase):

    def test_invalid_input(self):
        with self.assertRaises(FileNotFoundError):
            vid_to_frames("does/not/exist.mp4", "random")

    def test_writes_output(self):
        path_to_video = "tests/data/raw_videos/in/second.mp4"
        path_to_frames = "tests/data/raw_frames/out/vid_to_frames"

        vid_to_frames(path_to_video, path_to_frames)

        self.assertTrue(os.path.isdir(path_to_frames))

        num_expected_frames = 30
        # not_found_file is captured in a variable so we can ensure we remove the
        # output dir incase anything is missing instead of fatally failing
        # the assert
        not_found_file = ""
        for i in range(num_expected_frames):
            if not os.path.isfile(os.path.join(path_to_frames, "{:05d}.jpg".format(i))):
                not_found_file = os.path.join(path_to_frames, "{:05d}.jpg".format(i))

        shutil.rmtree(path_to_frames)
        self.assertEqual(not_found_file, "")


if __name__ == '__main__':
    unittest.main()
