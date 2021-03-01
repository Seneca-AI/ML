#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 20:50:40 2021
Cropping the images and looking for lanes
@author: sagar
"""


import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob

source_binary = "/media/sagar/New Volume/everything/job/Seneca/data/making_vid/binary_results/*"
import pandas as pd
names = []
lane_change = []
for i in sorted(glob.glob(source_binary)):
    s = 0
    img = cv2.imread(i,0)
    img = cv2.resize(img, (512,257), interpolation = cv2.INTER_AREA)
    X1 = int(img.shape[1]*1/4)+2
    X2 = int(img.shape[1]*3/4)
    Y1 = 211
    Y2 = len(img)
    cropped_area = img[Y1:Y2,X1:X2]
    unique_array = np.unique(cropped_area)
    element = [250,251,252,253,254,255]
    existing = np.isin(element, unique_array)
    print(i)
    name = i.split("/")[-1]
    for j in existing:
        #print(i)
        
        if j == True:
            s = 1
            break
        elif j == False:
            #s = 0
            continue
    names.append(name)
    lane_change.append(s)
    #break
dict = {'name_of_img': names, 'lane change (0/1)': lane_change}   
   
df = pd.DataFrame(dict)  
    
# saving the dataframe  
df.to_csv('./Image_names_and_lane_change_status.csv')  
    
            