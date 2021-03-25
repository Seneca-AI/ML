"""
CLI
1. cd testing
2. python -m unittest making_concurrent_frames_tusimple_test.py
The output should be
.
----------------------------------------------------------------------
Ran 1 test in 261.948s

OK
this is the unit test module for the making_the_concurrent_frames_Tusimple.py
"""

import unittest
import sys
import os
sys.path.append("../")
import glob
from utils.making_concurrent_frames_Tusimple import renaming_padding_if_in_folder_names

class TestMakingConcurrentFrames(unittest.TestCase):
    
    def test_output(self):
        source_dataset = "../data/frames/*/*"
        output_images = "../data/clips/"
        actual = renaming_padding_if_in_folder_names(Source = source_dataset,Dest = output_images)
        self.assertIsNotNone(actual)
            
    def test_output_type(self):
        source_dataset = "../data/frames/*/*"
        output_images = "../data/clips/"
        b = os.listdir(output_images)[0].split(".")[-1]
        a = "jpg"
        self.assertEqual(a,b)
        for i in os.listdir(output_images):
            os.remove(output_images + i)
    
    # TODO: add more tests