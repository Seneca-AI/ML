"""
CLI
python3 -m unittest yolov5_csv_combined.py
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
sys.path.append("../source_tailgating")
from evaluate_tailgating.yolov5_csv_combined import yolov5_csv_combined
import pandas as pd

class TestEvaluationMarkingLaneChanges(unittest.TestCase):
    
    def test_output(self):
        weights = "../source_tailgating/yolov5s.pt"
        source_images = "../data/too_close/images" 
        img_size = 1280 
        conf_thres = 0.25
        iou_thres = 0.45
        device = "cpu"
        labels = "../data/delete/too_close/labels/"
        save_txt = "text.txt"
        csv_destination = "../data/delete/csv/"
        csv_name = "too_close.csv"
        save_conf = False
        classes = None
        actual = yolov5_csv_combined(weights, source_images, 
                        img_size, conf_thres, iou_thres, 
                        device, save_txt, save_conf,
                        classes, labels, 
                        csv_destination = csv_destination + csv_name)
        self.assertIsNone(actual)
        
    def test_output_of_file(self):
        weights = "../source_tailgating/yolov5s.pt"
        source_images = "../data/too_close/images" 
        img_size = 1280 
        conf_thres = 0.25
        iou_thres = 0.45
        device = "cpu"
        labels = "../data/delete/too_close/labels/"
        save_txt = "text.txt"
        csv_destination = "../data/delete/csv/"
        csv_name = "too_close.csv"
        save_conf = False
        classes = None
        loaded_csv = pd.read_csv(csv_destination+csv_name)
        column1 = loaded_csv['name_of_img'].values.tolist()
        column2 = loaded_csv['too close (0/1)'].values.tolist()
        expected_column1 = ["1492636597661530888.jpg", "1492637188172803505.jpg", "1492637289078643492.jpg", "1492637368864044659.jpg", "1494452621490750553.jpg", "1494453387654539706.jpg", "1494453509599288732.jpg"]
        expected_column2 = [0,0,1,1,1,0,0]
        self.assertEqual(column1, expected_column1)
        self.assertEqual(column2, expected_column2)
    
    def test_output_type(self):
        weights = "../source_tailgating/yolov5s.pt"
        source_images = "../data/too_close/images" 
        img_size = 1280 
        conf_thres = 0.25
        iou_thres = 0.45
        device = "cpu"
        labels = "../data/delete/too_close/labels/"
        save_txt = "text.txt"
        csv_destination = "../data/delete/csv/"
        csv_name = "too_close.csv"
        save_conf = False
        classes = None
        actual_extension = sorted(os.listdir(csv_destination))[1].split(".")[-1]
        #TODO: add checking the length of the lists
        expected_extension = "csv"
        self.assertEqual(expected_extension,actual_extension)
        os.remove(csv_destination+ csv_name)