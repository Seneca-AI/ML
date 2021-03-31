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
from evaluate.check_and_mark_lane_changes import check_and_mark_lane_changes
import pandas as pd 

class TestMarkingLaneChanges(unittest.TestCase):
    
    def test_output(self):
        weights_path = "../BiseNetV2_LaneNet_Tusimple_Model_Weights/tusimple_lanenet.ckpt"
        binary_imgs_directory = "../data/binary_results/"
        csv_destination = "../data/delete/csv/"
        csv_name = "Image_names_and_lane_change_status.csv"
        if os.path.exists(binary_imgs_directory):
            pass
        else:
            os.mkdir(binary_imgs_directory)
        actual = check_and_mark_lane_changes(binary_imgs_directory + "*", csv_destination + csv_name)
        self.assertIsNone(actual)
        
    def test_output_name(self):
        weights_path = "../BiseNetV2_LaneNet_Tusimple_Model_Weights/tusimple_lanenet.ckpt"
        binary_imgs_directory = "../data/binary_results/"
        csv_destination = "../data/delete/csv/"
        csv_name = "Image_names_and_lane_change_status.csv"
        actual_name = os.listdir(csv_destination)[0]
        expected_name = csv_name
        self.assertEqual(expected_name,actual_name)
        
        # checks if the values of the csv are either 0/1 or something else
    def test_output_value(self):
        weights_path = "../BiseNetV2_LaneNet_Tusimple_Model_Weights/tusimple_lanenet.ckpt"
        binary_imgs_directory = "../data/binary_results/"
        csv_destination = "../data/delete/csv/"
        csv_name = "Image_names_and_lane_change_status.csv"
        loaded_csv = pd.read_csv(csv_destination + csv_name)
        column1 = loaded_csv['name_of_img']
        column2 = loaded_csv['lane change (0/1)']
        for i in column1:
            self.assertEqual(i.split(".")[-1],"jpg")
        for i in column2:
            if i == 0 or i ==1:
                pass
            else:
                raise Exception("The too close value does not have the required 0 or 1 value")
        os.remove(csv_destination + csv_name)
    
    # TODO: add more tests
        