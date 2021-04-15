"""
CLI
python3 -m unittest evaluation_lane_csv_making_combined_test.py
"""


import unittest
import sys
import os
sys.path.append("../")
import cv2
import glob
import numpy as np
import pandas as pd 
import glob

from evaluate.evaluation_lane_csv_making_combined import evaluation_lane_csv_making_combined

class TestEvaluationMarkingLaneChanges(unittest.TestCase):
    
    def test_output(self):
        image_dir = "../data/clips"
        weights_path = "../BiseNetV2_LaneNet_Tusimple_Model_Weights/tusimple_lanenet.ckpt"
        save_dir = "../data/delete/results/"
        save_dir_binary = "../data/delete/binary_results/"
        csv_destination = "../data/delete/csv/"
        csv_name = "Image_names_and_lane_change_status_vid_2.csv"
        actual = evaluation_lane_csv_making_combined(src_dir = image_dir,
                                            weights_path = weights_path,
                                            save_dir = save_dir,
                                            save_dir_binary = save_dir_binary, source_binary = save_dir_binary + "*", 
                                            csv_destination= csv_destination + csv_name)
        self.assertIsNone(actual)
        
    def test_output_name(self):
        image_dir = "../data/clips"
        weights_path = "../BiseNetV2_LaneNet_Tusimple_Model_Weights/tusimple_lanenet.ckpt"
        save_dir = "../data/delete/results/"
        save_dir_binary = "../data/delete/binary_results/"
        csv_destination = "../data/delete/csv/"
        csv_name = "Image_names_and_lane_change_status_vid_2.csv"
        actual_name = sorted(os.listdir(csv_destination))[1]
        expected_name = csv_name
        self.assertEqual(expected_name,actual_name)
        
    def test_output_value(self):
        image_dir = "../data/clips"
        weights_path = "../BiseNetV2_LaneNet_Tusimple_Model_Weights/tusimple_lanenet.ckpt"
        save_dir = "../data/delete/results/"
        save_dir_binary = "../data/delete/binary_results/"
        csv_destination = "../data/delete/csv/"
        csv_name = "Image_names_and_lane_change_status_vid_2.csv"
        loaded_csv = pd.read_csv(csv_destination + csv_name)
        column1_expected = ["00021.jpg", "00022.jpg", "00051.jpg", "00052.jpg", "00259.jpg"]
        column1 = loaded_csv['name_of_img'].values.tolist()
        column2_expected = [0, 0, 0, 0, 1]
        column2 = loaded_csv['lane change (0/1)'].values.tolist()
        self.assertEqual(column1, column1_expected)
        self.assertEqual(column2, column2_expected)
        os.remove(csv_destination + csv_name)

    # TODO: add more tests