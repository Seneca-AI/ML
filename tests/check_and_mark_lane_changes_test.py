"""
CLI
1. cd testing
2. python -m unittest check_and_mark_lane_changes_test.py
The output should be
.
----------------------------------------------------------------------
Ran 2 tests in 261.948s

OK
this is the unit test module for the check_and_mark_lane_changes_test.py
"""

import unittest
import sys
import os
sys.path.append("../")
import glob
from utils.making_concurrent_frames_tusimple import renaming_padding_if_in_folder_names
from evaluate.evaluate_vid_on_lanenet import evaluate_vid_on_lanenet
from evaluate.check_and_mark_lane_changes import check_and_mark_lane_changes
import pandas as pd 

class TestMarkingLaneChanges(unittest.TestCase):
    
    def test_output(self):
        img_dir = "../data/frames/*/*"
        src_dir = "../data/clips/"
        weights_path = "../BiseNetV2_LaneNet_Tusimple_Model_Weights/tusimple_lanenet.ckpt"
        save_dir = "../data/results/"
        save_dir_binary = "../data/binary_results/"
        csv_destination = "../extras/"
        csv_name = "Image_names_and_lane_change_status.csv"
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
        actual = check_and_mark_lane_changes(save_dir_binary + "/*", csv_destination + csv_name)
        self.assertIsNone(actual)
        
    def test_output_type(self):
        img_dir = "../data/frames/*/*"
        src_dir = "../data/clips/"
        weights_path = "../BiseNetV2_LaneNet_Tusimple_Model_Weights/tusimple_lanenet.ckpt"
        save_dir = "../data/results/"
        save_dir_binary = "../data/binary_results/"
        csv_destination = "../extras/"
        csv_name = "Image_names_and_lane_change_status.csv"
        b = os.listdir(csv_destination)[0].split(".")[-1]
        a = "csv"
        self.assertEqual(a,b)
        
    def test_output_value(self):
        img_dir = "../data/frames/*/*"
        src_dir = "../data/clips/"
        weights_path = "../BiseNetV2_LaneNet_Tusimple_Model_Weights/tusimple_lanenet.ckpt"
        save_dir = "../data/results/"
        save_dir_binary = "../data/binary_results/"
        csv_destination = "../extras/Image_names_and_lane_change_status.csv"
        loaded_csv = pd.read_csv(csv_destination)
        column1 = loaded_csv['name_of_img']
        column2 = loaded_csv['lane change (0/1)']
        for i in column1:
            self.assertEqual(i.split(".")[-1],"jpg")
        for i in column2:
            i = str(i) 
            if i == "0":
                self.assertEqual(i, "0")
            elif i == "1":
                self.assertEqual(i, "1")
            else:
                raise Exception("The too close value does not have the required 0 or 1 value")
                
    def test_run_and_clear(self):
        img_dir = "../data/frames/*/*"
        src_dir = "../data/clips/"
        weights_path = "../BiseNetV2_LaneNet_Tusimple_Model_Weights/tusimple_lanenet.ckpt"
        save_dir = "../data/results/"
        save_dir_binary = "../data/binary_results/"
        csv_destination = "../extras/Image_names_and_lane_change_status.csv"
        for i in os.listdir(src_dir):
            os.remove(src_dir + i)
        for i in os.listdir(save_dir):
            os.remove(save_dir + i)
        for i in os.listdir(save_dir_binary):
            os.remove(save_dir_binary + i) 
        os.remove(csv_destination)
    
    # TODO: add more tests
        