"""
CLI
1. cd testing
2. python3 -m unittest making_concurrent_frames_tusimple_test.py
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
from utils.making_concurrent_frames_tusimple import renaming_padding_if_in_folder_names

class TestMakingConcurrentFrames(unittest.TestCase):
    
    def test_output(self):
        source_dataset = "../data/frames/*/*"
        output_images = "../data/delete/"
        actual = renaming_padding_if_in_folder_names(Source = source_dataset,Dest = output_images)
        self.assertIsNotNone(actual)
            
    def test_output_values(self):
        source_dataset = "../data/frames/*/*"
        output_images = "../data/delete/"
        b = sorted(os.listdir(output_images))
        a = ['.gitignore','21.jpg', '22.jpg', '51.jpg', '52.jpg']
        self.assertEqual(a,b)
        for i in glob.glob(output_images + "*.jpg"):
            os.remove(i)
    
    # TODO: add more tests
