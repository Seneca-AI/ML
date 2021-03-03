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
def renaming_padding_if_in_folder_names(Source,Dest):
    """
    

    Parameters
    ----------
    Source : string
        It is the Source of where you want your frames from. It is the Main Folder in the below example.
        The directory for this is in:-
       Main Folder 
       |-Folder 1
        |
        |-Folder 1a
            |
            |-Images
        |-Folder 1b
        Folder 2
        |
        |-Folder 1a
            |
            |-Images
        |-Folder 1b
    Dest : string
        Main Folder
        |- Images with names sorted and combined.

    Returns
    -------
    images: save images with renamed and in the indicated directories
    hi : list
        It is a list of all the images that we just sorted and renamed

    """
    names = []
    for i in glob.glob(Source):
        #img = cv2.imread(i)
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
        #cv2.imwrite(Dest + new_name + ".jpg", img)
    hi = sorted(names)
    return hi
#%% for binary masks for converting the 60_1 numbered images into sorted thing

Source = "/media/sagar/New Volume/everything/job/Seneca/data/making_vid/binary_results_wrong_format/*"
Dest = "/media/sagar/New Volume/everything/job/Seneca/data/making_vid/binary_results/"
def renaming_by_adding_number_names(Source,Dest):
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
    return hi
