"""
CLI
1. cd testing
2. python -m unittest evaluate_vid_on_lanenet_test.py
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
from evaluate.evaluate_vid_on_lanenet import evaluate_vid_on_lanenet
import cv2
import glob
import numpy as np

class TestEvaluatingVidOnLanenet(unittest.TestCase):
    
    def test_output(self):
        src_dir = "../data/clips/"
        weights_path = "../BiseNetV2_LaneNet_Tusimple_Model_Weights/tusimple_lanenet.ckpt"
        save_dir = "../data/delete/results/"
        save_dir_binary = "../data/delete/binary_results/"
        if os.path.exists(save_dir):
            pass
        else:
            os.mkdir(save_dir)
        if os.path.exists(save_dir_binary):
            pass
        else:
            os.mkdir(save_dir_binary)
        actual = evaluate_vid_on_lanenet(src_dir, weights_path, save_dir,save_dir_binary)
        self.assertIsNone(actual)
        
    def test_output_type(self):
        src_dir = "../data/clips/"
        weights_path = "../BiseNetV2_LaneNet_Tusimple_Model_Weights/tusimple_lanenet.ckpt"
        save_dir = "../data/delete/results/"
        save_dir_binary = "../data/delete/binary_results/"
        actual_extension = os.listdir(save_dir_binary)[0].split(".")[-1]
        expected_extension = "jpg"
        self.assertEqual(expected_extension,actual_extension)
        
    # checks if the all images are having specified values(binary images) or not
    def test_output_value(self):
        src_dir = "../data/clips/"
        weights_path = "../BiseNetV2_LaneNet_Tusimple_Model_Weights/tusimple_lanenet.ckpt"
        save_dir = "../data/delete/results/"
        save_dir_binary = "../data/delete/binary_results/"
        for i in glob.glob(save_dir_binary + "*"):
            img = cv2.imread(i)
            len_of_unique_values = len(np.unique(img))
            if len_of_unique_values > 30: # normal image have more than 100 values. Binary image made by lanenet has less than 20 values
                raise Exception("The images have way too many values to be a binary image")
        for i in os.listdir(save_dir):
            os.remove(save_dir + i)
        for i in os.listdir(save_dir_binary):
            os.remove(save_dir_binary + i) 
        
    # TODO: add more tests
