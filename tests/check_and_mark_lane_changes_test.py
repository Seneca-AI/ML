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
from utils.converting_frames_to_vids import frame_to_vids
from utils.making_concurrent_frames_Tusimple import renaming_padding_if_in_folder_names
from utils.converting_video_to_frames import video_to_frames
from evaluate.evaluate_vid_on_lanenet import evaluate_vid_on_lanenet
from evaluate.check_and_mark_lane_changes import check_and_mark_lane_changes

class TestMarkingLaneChanges(unittest.TestCase):
    
    def test_output(self):
        img_dir = "../data/frames/*/*"
        src_dir = "../data/clips/"
        weights_path = "../BiseNetV2_LaneNet_Tusimple_Model_Weights/tusimple_lanenet.ckpt"
        save_dir = "../data/results/"
        save_dir_binary = "../data/binary_results/"
        csv_destination = "../extras/Image_names_and_lane_change_status.csv"
        if os.path.exists(save_dir):
            pass
        else:
            os.mkdir(save_dir)
        if os.path.exists(save_dir_binary):
            pass
        else:
            os.mkdir(save_dir_binary)
        renaming_padding_if_in_folder_names(Source = img_dir,Dest = src_dir)
        evaluate_vid_on_lanenet(src_dir, weights_path, save_dir,save_dir_binary)
        actual = check_and_mark_lane_changes(save_dir_binary, csv_destination)
        self.assertIsNone(actual)
        
    def test_output_type(self):
        img_dir = "../data/frames/*/*"
        src_dir = "../data/clips/"
        weights_path = "../BiseNetV2_LaneNet_Tusimple_Model_Weights/tusimple_lanenet.ckpt"
        save_dir = "../data/results/"
        save_dir_binary = "../data/binary_results/"
        csv_destination = "../extras/Image_names_and_lane_change_status.csv"
        b = os.listdir(csv_destination)[0].split(".")[-1]
        a = "jpg"
        self.assertEqual(a,b)
        for i in os.listdir(src_dir):
            os.remove(src_dir + i)
        for i in os.listdir(save_dir):
            os.remove(save_dir + i)
        for i in os.listdir(save_dir_binary):
            os.remove(save_dir_binary + i) 
        os.remove(csv_destination)
    
    # TODO: add more tests
        