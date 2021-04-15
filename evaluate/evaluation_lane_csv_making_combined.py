"""
CLI
python3 evaluation_lane_csv_making_combined.py --image_dir ../data/clips --weights_path ../BiseNetV2_LaneNet_Tusimple_Model_Weights/tusimple_lanenet.ckpt --save_dir ../data/delete/results/ --save_dir_binary ../data/delete/binary_results/ --CSV_destination ../data/delete/csv/Image_names_and_lane_change_status_vid_2.csv 
combined evaluation and lane change markings
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
import pandas as pd
import argparse
import warnings

import argparse
import glob
import os
import os.path as ops
import time

import tensorflow as tf
import tqdm
import sys
sys.path.append("../")

from source.lanenet_model import lanenet
from source.lanenet_model import lanenet_postprocess
from source.local_utils.config_utils import parse_config_utils
from source.local_utils.log_util import init_logger

from evaluate.evaluate_vid_on_lanenet import evaluate_vid_on_lanenet
from evaluate.check_and_mark_lane_changes import check_and_mark_lane_changes

CFG = parse_config_utils.lanenet_cfg
LOG = init_logger.get_logger(log_file_name_prefix='lanenet_eval_vid')

def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_dir', type=str, default = "../data/clips",help='The source tusimple lane test data dir')
    parser.add_argument('--weights_path', type=str, default= "../BiseNetV2_LaneNet_Tusimple_Model_Weights/tusimple_lanenet.ckpt",help='The model weights path')
    parser.add_argument('--save_dir', type=str,default = "../data/delete/results/", help='The test output save root dir')
    parser.add_argument('--save_dir_binary', type=str,default = "../data/delete/binary_results/", help='The test output save root dir')
    parser.add_argument('--csv_destination', type=str, default= '../data/delete/csv/Image_names_and_lane_change_status_vid_2.csv',help='path to where you wish to save the frames for the output of second type of dataset')
    return parser.parse_args()

def evaluation_lane_csv_making_combined(src_dir, weights_path, save_dir,save_dir_binary, source_binary, csv_destination):
    evaluate_vid_on_lanenet(src_dir, weights_path, save_dir,save_dir_binary)
    check_and_mark_lane_changes(source_binary, csv_destination)

    for i in glob.glob(save_dir + "*.jpg"):
        os.remove(i)
    for i in glob.glob(save_dir_binary + "*.jpg"):
        os.remove(i)

if __name__ == '__main__':
    args = init_args()
    evaluation_lane_csv_making_combined(src_dir=args.image_dir,
        weights_path=args.weights_path,
        save_dir=args.save_dir,
        save_dir_binary = args.save_dir_binary, source_binary = args.save_dir_binary + "*", 
        csv_destination= args.csv_destination)
    for i in glob.glob(args.save_dir + "*.jpg"):
        os.remove(i)
    for i in glob.glob(args.save_dir_binary + "*.jpg"):
        os.remove(i)
        