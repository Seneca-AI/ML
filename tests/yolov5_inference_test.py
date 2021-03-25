"""
CLI
python3 -m unittest yolov5_inference_test.py
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
        actual = detect(weights, source, imgsz, conf_thres, iou_thres, device, save_txt, save_conf, classes, output_folder)
        self.assertIsNone(actual)
        
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
        actual = detect(weights, source, imgsz, conf_thres, iou_thres, device, save_txt, save_conf, classes, output_folder)
        b = os.listdir(output_folder + "labels/")[0].split(".")[-1]
        a = "txt"
        self.assertEqual(a,b)
        for i in os.listdir(output_folder):
            for j in os.listdir(output_folder + "images/"):
                os.remove(output_folder + "images/" + j)
            for k in os.listdir(output_folder + "labels/"):
                os.remove(output_folder + "labels/" + k)
            
    # TODO: add more tests