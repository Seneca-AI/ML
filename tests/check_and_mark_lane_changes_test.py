"""
CLI
1. cd testing
2. python3 -m unittest check_and_mark_lane_changes_test.py
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
        actual_name = sorted(os.listdir(csv_destination))[1]
        expected_name = csv_name
        self.assertEqual(expected_name,actual_name)
        
    # checks if the values of the csv are correct or not
    def test_output_value(self):
        weights_path = "../BiseNetV2_LaneNet_Tusimple_Model_Weights/tusimple_lanenet.ckpt"
        binary_imgs_directory = "../data/binary_results/"
        csv_destination = "../data/delete/csv/"
        csv_name = "Image_names_and_lane_change_status.csv"
        loaded_csv = pd.read_csv(csv_destination + csv_name)
        column1_expected = ["00021.jpg", "00022.jpg", "00051.jpg", "00052.jpg", "00259.jpg"]
        column1 = loaded_csv['name_of_img'].values.tolist()
        column2_expected = [0, 0, 0, 0, 1]
        column2 = loaded_csv['lane change (0/1)'].values.tolist()
        self.assertEqual(column1, column1_expected)
        self.assertEqual(column2, column2_expected)
        os.remove(csv_destination + csv_name)
    # TODO: add more tests
