"""
CLI
python3 yolov5_csv_combined.py --source_images ../data/too_close/images --img_size 1280 --conf_thres 0.25 --iou_thres 0.45 --device "0" --labels ../data/delete/too_close/labels/ --csv_destination ../data/delete/csv/Image_names_and_too_close_status.csv
"""

import argparse
import time
from pathlib import Path

import cv2
import torch
from numpy import random
import sys
import warnings
sys.path.append("../source_tailgating")
sys.path.append("../")
from models.experimental import attempt_load
from utils.datasets import LoadImages
from utils.general import check_img_size, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized

import numpy as np
import glob,os
import pandas as pd
sys.path.append("../")
from evaluate_tailgating.yolov5_inference import detect
from evaluate_tailgating.making_csv_of_too_close import making_csv_of_too_close

def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default='../source_tailgating/yolov5s.pt', help='model.pt path(s)')
    parser.add_argument('--source_images', type=str, default = '../data/too_close/images',help='The path to the input images ')
    parser.add_argument('--img_size', type=int, default=1280, help='inference size (pixels)')
    parser.add_argument('--conf_thres', type=float, default=0.25, help='object confidence threshold')
    parser.add_argument('--iou_thres', type=float, default=0.45, help='IOU threshold for NMS')
    parser.add_argument('--device', default='0', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--save_txt', action='store_true', default = "text.txt",help='save results to *.txt')
    parser.add_argument('--save_conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
    parser.add_argument('--labels', default='../data/delete/too_close/labels/', help='where you wish to save the labels')
    parser.add_argument('--csv_destination', type=str, default= '../data/delete/csv/Image_names_and_too_close_status.csv',help='path to where you wish to save the csv file')
    return parser.parse_args()

def yolov5_csv_combined(weights, source_images, img_size, conf_thres, iou_thres, device, save_txt, 
                        save_conf, classes, labels, csv_destination):
    detect(weights, source_images, img_size, conf_thres, iou_thres, device, save_txt, save_conf, classes, labels)
    making_csv_of_too_close(source_images + "/*.jpg", labels, csv_destination)
    for i in glob.glob(labels + "labels/*.txt"):
        os.remove(i)
    for i in glob.glob(labels + "images/*.jpg"):
        os.remove(i)    
        
if __name__ == '__main__':
    args = init_args()
    yolov5_csv_combined(weights = args.weights, source_images = args.source_images, 
                        img_size = args.img_size, conf_thres = args.conf_thres, iou_thres = args.iou_thres, 
                        device = args.device, save_txt = args.save_txt, save_conf = args.save_conf,
                        classes = args.classes, labels = args.labels, 
                        csv_destination = args.csv_destination)
    for i in glob.glob(args.labels + "labels/*.txt"):
        os.remove(i)
    for i in glob.glob(args.labels + "images/*.jpg"):
        os.remove(i)    
        