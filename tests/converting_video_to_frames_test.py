"""
CLI
1. cd testing
2. python3 -m unittest converting_video_to_frames_test.py
The output should be
.
----------------------------------------------------------------------
Ran 2 tests in 261.948s

OK
this is the unit test module for the converting_video_to_frames.py
"""

import unittest
import sys
import os
sys.path.append("../")
import glob
from utils.converting_video_to_frames import video_to_frames

class TestVidsToFrames(unittest.TestCase):
    
    def test_output(self):
        input_vid = "clip1.avi"
        input_vid_location = "../data/vid/"
        output_images_from_vid = "../data/delete/clips"
        actual = video_to_frames(input_loc = input_vid_location + input_vid, output_loc = output_images_from_vid + "/")
        self.assertIsNone(actual)
        
    def test_output_values(self):
        input_vid = "clip1.avi"
        input_vid_location = "../data/vid/"
        output_images_from_vid = "../data/delete/clips"
        actual_outputs = sorted(os.listdir(output_images_from_vid))
        expected = ['.gitignore',"00001.jpg", '00002.jpg', '00003.jpg']
        self.assertEqual(expected,actual_outputs)
        for i in glob.glob(output_images_from_vid + "/*.jpg"):
            os.remove(i)
    
    # TODO: add more tests
