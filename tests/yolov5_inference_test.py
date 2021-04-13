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
import glob
import cv2
import torch
from numpy import random
import os
import sys
sys.path.append("../")
from evaluate_tailgating.yolov5_inference import detect
import filecmp

class TestEvaluatingVidOnLanenet(unittest.TestCase):
    
    def test_output(self):
        weights = "../source_tailgating/yolov5s.pt"
        source = "../data/too_close/images" 
        imgsz = 1280 
        conf_thres = 0.25
        iou_thres = 0.45
        device = "cpu"
        output_folder = "../data/delete/too_close/labels/"
        save_txt = "text.txt"
        save_conf = False
        classes = None
        actual = detect(weights, source, imgsz, conf_thres, iou_thres, device, save_txt, save_conf, classes, output_folder)
        self.assertIsNone(actual)
        
    # this test is used for checking if all the images have got their text files (the vehicle labels) or not. 
    # It gives error if any of the images do not have their txt files.
    def test_output_type(self):
        source = "../data/too_close/images"
        output_folder = "../data/delete/too_close/labels/"
        save_txt = "text.txt"
        names_of_texts = []
        for i in glob.glob(source + "/*"):
            names_of_texts.append(i.split("/")[-1].split(".")[0] + ".txt")
        names_of_texts = sorted(names_of_texts)
        expected_labels = []
        for i in glob.glob(output_folder + "labels/*"):
            expected_labels.append(i.split("/")[-1])
        expected_labels = sorted(expected_labels)
        self.assertEqual(names_of_texts,expected_labels)

    def test_output_value(self):
        source = "../data/too_close/images"
        output_folder = "../data/delete/too_close/labels/"
        labels_output_directory = "../data/delete/too_close/labels/labels/*"
        labels_directory = "../data/labels/"
        a = glob.glob(labels_directory+ "/labels/*")
        b = glob.glob(output_folder + "labels/*")
        for i in a:
            for j in b:
                f1 = open(i, "r")
                f2 = open(j, "r")
                for line1,line2 in zip(f1,f2): 
                    if line1 == line2: 
                        continue
                    else:
                        break 
                f1.close() 
                f2.close()
        for i in glob.glob(output_folder + "images/*.jpg"):
            os.remove(i)
        for j in glob.glob(output_folder + "labels/*.txt"):
            os.remove(j)
            
    # TODO: add more tests
