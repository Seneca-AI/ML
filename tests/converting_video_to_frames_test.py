"""
CLI
1. cd testing
2. python -m unittest converting_video_to_frames_test.py
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
        output_images_from_vid = "../data/delete/extracted_frames"
        video_to_frames(input_loc = input_vid_location + input_vid, output_loc = output_images_from_vid + "/")
        self.assertIsNone(actual)
        
    def test_output_values(self):
        input_vid = "clip1.avi"
        input_vid_location = "../data/vid/"
        output_images_from_vid = "../data/delete/extracted_frames"
        actual_outputs = os.listdir(output_images_from_vid)
        expected = ["00001.jpg", '00002.jpg', '00003.jpg', '.gitignore']
        self.assertCountEqual(expected,actual_outputs)
        for i in os.listdir(output_images_from_vid):
            os.remove(output_images_from_vid +"/"+i)
    
    # TODO: add more tests