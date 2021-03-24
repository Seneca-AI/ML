"""
sample CLI
python3 check_and_mark_lane_changes.py --source_binary_images ./binary_results2 --CSV_destination ../extras/Image_names_and_lane_change_status_vid_2.csv
Cropping the images and looking for lanes
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
import pandas as pd
import argparse

def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source_binary_images', type=str, default = "/media/sagar/New Volume/everything/job/Seneca/data/making_vid/binary_results2/*",help='The path to the input dataset for second type of dataset')
    parser.add_argument('--CSV_destination', type=str, default= '../extras/Image_names_and_lane_change_status_vid_2.csv',help='path to where you wish to save the frames for the output of second type of dataset')
    return parser.parse_args()

def check_and_mark_lane_changes(source_binary, CSV_destination):
    """
    This function reads a directory of images, evaluates each image on whether 
    or not the driver is in the middle of a lane change by checking if the lane 
    line is within a bounded box, and stores the output (1 = changing_lanes, 0 = !changing_lanes) 
    in a CSV file against name of every frame.    

    Parameters
    ----------
    source_binary : str
        DESCRIPTION. Give the path to the binary files (generated by the code evaluate_vid_on_lanenet.py) as the location
    CSV_destination :str
        DESCRIPTION. Give the name and location of the csv folder. 

    Returns
    -------
    None
    Makes the csv of the frames name vs lane change instances

    """
    names = []
    lane_change = []
    for i in sorted(glob.glob(source_binary)):
        s = 0
        img = cv2.imread(i,0)
        size = (512,256)
        img = cv2.resize(img, size, interpolation = cv2.INTER_AREA)
        
        # from experimentation these are the values of the BBOX
        X1 = int(img.shape[1]*1/4)+2
        X2 = int(img.shape[1]*3/4)
        Y1 = 211 
        Y2 = len(img)
        
        cropped_area = img[Y1:Y2,X1:X2]
        unique_array = np.unique(cropped_area)
        
        # these are the values that are given by the evaluate_vid_on_lanenet.py
        element = [250,251,252,253,254,255] 
        
        existing = np.isin(element, unique_array)
        
        name = i.split("/")[-1]
        for j in existing:
            if j == True:
                s = 1
                break
            elif j == False:
                continue
        names.append(name)
        lane_change.append(s)
    dict = {'name_of_img': names, 'lane change (0/1)': lane_change}   
    df = pd.DataFrame(dict)  
        
    # saving the dataframe  
    df.to_csv(CSV_destination)

if __name__ == '__main__':
    args = init_args()
    check_and_mark_lane_changes(source_binary = args.source_binary_images, CSV_destination= args.CSV_destination)
