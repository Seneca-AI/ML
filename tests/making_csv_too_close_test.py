"""
CLI
python3 -m unittest making_csv_too_close_test.py
Result

.
----------------------------------------------------------------------
Ran 2 tests in 4.568s

OK

"""

import unittest
import glob

import cv2
import torch
from numpy import random
import os
import sys
sys.path.append("../")
from evaluate_tailgating.making_csv_of_too_close import making_csv_of_too_close
import pandas as pd

class TestEvaluatingVidOnLanenet(unittest.TestCase):
    
    def test_output(self):
        weights = "../source_tailgating/yolov5s.pt"
        source = "../data/too_close/images"
        imgsz = 1280 
        conf_thres = 0.25
        iou_thres = 0.45
        device = ""
        output_folder = "../data/labels/"
        save_txt = "text.txt"
        save_conf = False
        classes = None
        CSV_destination = "../data/delete/csv/"
        csv_name = "too_close.csv"
        actual = making_csv_of_too_close(source_images = source + "/*", source_labels = output_folder , CSV_destination = CSV_destination+csv_name)
        self.assertIsNone(actual)
        
    # testing the values of csv
    def test_output_of_file(self):
        weights = "../source_tailgating/yolov5s.pt"
        source = "../data/too_close/images" 
        imgsz = 1280 
        conf_thres = 0.25
        iou_thres = 0.45
        device = ""
        output_folder = "../data/labels/"
        save_txt = "text.txt"
        save_conf = False
        classes = None
        CSV_destination = "../data/delete/csv/"
        csv_name = "too_close.csv"
        loaded_csv = pd.read_csv(CSV_destination+csv_name)
        column1 = loaded_csv['name_of_img'].values.tolist()
        column2 = loaded_csv['too close (0/1)'].values.tolist()
        expected_column1 = ["1492636597661530888.jpg", "1492637188172803505.jpg", "1492637289078643492.jpg", "1492637368864044659.jpg", "1494452621490750553.jpg", "1494453387654539706.jpg", "1494453509599288732.jpg"]
        expected_column2 = [0,0,1,1,1,0,0]
        self.assertEqual(column1, expected_column1)
        self.assertEqual(column2, expected_column2)

    def test_output_type(self):
        weights = "../source_tailgating/yolov5s.pt"
        source = "../data/too_close/images" 
        imgsz = 1280 
        conf_thres = 0.25
        iou_thres = 0.45
        device = ""
        output_folder = "../data/labels/"
        save_txt = "text.txt"
        save_conf = False
        classes = None
        CSV_destination = "../data/delete/csv/"
        csv_name = "too_close.csv"
        actual_extension = sorted(os.listdir(CSV_destination))[1].split(".")[-1]
        #TODO: add checking the length of the lists
        expected_extension = "csv"
        self.assertEqual(expected_extension,actual_extension)
        os.remove(CSV_destination+ csv_name)

    # TODO: add more tests
