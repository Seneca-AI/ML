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
from evaluate_tailgating.yolov5_inference import detect
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
        output_folder = "../data/too_close/labels/"
        save_txt = "text.txt"
        save_conf = False
        classes = None
        CSV_destination = "../extras_tailgating/"
        csv_name = "too_close.csv"
        detect(weights, source, imgsz, conf_thres, iou_thres, device, save_txt, save_conf, classes, output_folder)
        actual = making_csv_of_too_close(source_images = source + "/*", source_labels = output_folder , CSV_destination = CSV_destination+csv_name)
        self.assertIsNone(actual)

    def test_output_of_file(self):
        weights = "../source_tailgating/yolov5s.pt"
        source = "../data/too_close/images" 
        imgsz = 1280 
        conf_thres = 0.25
        iou_thres = 0.45
        device = ""
        output_folder = "../data/too_close/labels/"
        save_txt = "text.txt"
        save_conf = False
        classes = None
        CSV_destination = "../extras_tailgating/"
        csv_name = "too_close.csv"
        loaded_csv = pd.read_csv(CSV_destination+csv_name)
        column1 = loaded_csv['name_of_img']
        column2 = loaded_csv['too close (0/1)']
        for i in column1:
            self.assertEqual(i.split(".")[-1],"jpg")
        for i in column2:
            if i== 0 or i==1:
                pass
            else:
                raise Exception("The too close value does not have the required 0 or 1 value")

    def test_output_type(self):
        weights = "../source_tailgating/yolov5s.pt"
        source = "../data/too_close/images" 
        imgsz = 1280 
        conf_thres = 0.25
        iou_thres = 0.45
        device = ""
        output_folder = "../data/too_close/labels/"
        save_txt = "text.txt"
        save_conf = False
        classes = None
        CSV_destination = "../extras_tailgating/"
        csv_name = "too_close.csv"
        detect(weights, source, imgsz, conf_thres, iou_thres, device, save_txt, save_conf, classes, output_folder)
        making_csv_of_too_close(source_images = source + "/*", source_labels = output_folder, CSV_destination = CSV_destination+csv_name)
        b = os.listdir(CSV_destination)[0].split(".")[-1]
        a = "csv"
        self.assertEqual(a,b)
        for i in os.listdir(output_folder):
            for j in os.listdir(output_folder + "images/"):
                os.remove(output_folder + "images/" + j)
            for k in os.listdir(output_folder + "labels/"):
                os.remove(output_folder + "labels/" + k)
        os.remove(CSV_destination+ csv_name)

    # TODO: add more tests