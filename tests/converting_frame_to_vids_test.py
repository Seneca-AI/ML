"""
CLI
1. cd testing
2. python3 -m unittest converting_frame_to_vids_test.py
The output should be
.
----------------------------------------------------------------------
Ran 1 test in 261.948s

OK
this is the unit test module for the converting_frame_to_vids.py
"""

import unittest
import sys
import os
sys.path.append("../")
import glob
from utils.converting_frames_to_vids import frame_to_vids

class TestFrameToVids(unittest.TestCase):
    
    def test_output(self):
        input_images = "../data/clips/"
        output_vid = "clip1.avi"
        output_vid_location = "../data/delete/"
        actual = frame_to_vids(source = input_images + "*",output_vid_name = output_vid_location + output_vid)
        self.assertIsNone(actual)
        
    def test_output_value(self):
        input_images = "../data/clips/"
        output_vid = "clip1.avi"
        output_vid_location = "../data/delete/"
        actual_output = os.listdir(output_vid_location)[1]
        expected = "clip1.avi"
        self.assertIn(expected, actual_output)
        os.remove(output_vid_location + output_vid)
    
    # TODO: add more tests
