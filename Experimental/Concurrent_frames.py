#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The code is used for renaming the images if they are in any other form. Use only one of the below functions
"""

import cv2
import glob
import os
import numpy as np
import argparse
def init_args():
    """
    for the CLI
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--source_dataset_2', type=str, default = "/media/sagar/New Volume/everything/job/Seneca/data/making_vid/binary_results_wrong_format/*",help='The path to the input dataset for second type of dataset')
    parser.add_argument('--output_images_2', type=str, default= "/media/sagar/New Volume/everything/job/Seneca/data/making_vid/binary_results/",help='path to where you wish to save the frames for the output of second type of dataset')
    return parser.parse_args()

def renaming_by_adding_number_names(Source2,Dest2):
    """
    Parameters
    ----------
    Source : string
        It is the source where you want to take the frames from. The frames have names in the form of 60_1 and are in the below directory.
        Main Folder 
       |-Folder 1
            |-60_1.jpg

       |-Folder 2
            |-246_1.jpg
        |-Folder 1b
    Dest : string
        Give the address of the folder where you wish to put the images

    Returns
    -------
    Gives images in destination. 
    Also returns the list of the images that have just been stored.

    """    
    names = []
    for i in glob.glob(Source2):
        img = cv2.imread(i)
        name1 = i.split("/")[-1].split("_")[0]
        name2 = i.split("/")[-1].split("_")[1].split(".")[0]
        name = str(int(name1) + int(name2))
        if len(name) == 1:
            new_name = "000"+ name
        if len(name) == 2:
            new_name = "00" + name
        if len(name) == 3:
            new_name = "0" + name
        if len(name) == 4:
            new_name = name
    
        names.append(new_name)
        cv2.imwrite(Dest2 + new_name + ".jpg", img)
    hi = sorted(names)
    return hi

if __name__ == '__main__':
    args = init_args()
    renaming_by_adding_number_names(Source2 = args.source_dataset_2,Dest2 = args.output_images_2)
