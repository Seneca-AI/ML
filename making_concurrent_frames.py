#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 20:25:26 2021

@author: sagar
"""

import cv2
import glob
import os
import numpy as np
#%% for changing the tusimple folder in folder images to concurrent folder
Source = "/media/sagar/New Volume/everything/job/Seneca/data/making_vid/frames2/*/*"
Dest = "/media/sagar/New Volume/everything/job/Seneca/data/making_vid/clips/"
l1 = glob.glob(Source)
names = []
for i in glob.glob(Source):
    img = cv2.imread(i)
    #print(i)
    
    name = str(int(i.split("/")[-2])+int((i.split("/")[-1]).split(".")[0]))
    if len(name) == 1:
        new_name = "000"+ name
    if len(name) == 2:
        new_name = "00" + name
    if len(name) == 3:
        new_name = "0" + name
    if len(name) == 4:
        new_name = name

    print(new_name)
    names.append(new_name)
    cv2.imwrite(Dest + new_name + ".jpg", img)
hi = sorted(names)
#%% for binary masks for converting the 60_1 numbered images into sorted thing

Source = "/media/sagar/New Volume/everything/job/Seneca/data/making_vid/binary_results_wrong_format/*"
Dest = "/media/sagar/New Volume/everything/job/Seneca/data/making_vid/binary_results/"
l1 = glob.glob(Source)
names = []
for i in glob.glob(Source):
    img = cv2.imread(i)
    #print(i)
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

    print(new_name)
    names.append(new_name)
    cv2.imwrite(Dest + new_name + ".jpg", img)
hi = sorted(names)
