#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 18:47:22 2021
Making vid from images
@author: sagar
"""

import cv2
import numpy as np
import glob


def frame_to_vids(source,output_vid_name):
    """
    

    Parameters
    ----------
    source : TYPE
        DESCRIPTION.
    output_vid_name : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    img_array = []
    for filename in sorted(glob.glob(source)):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
    
    
    out = cv2.VideoWriter(output_vid_name,cv2.VideoWriter_fourcc(*'DIVX'), 30, size)
     
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()
#%% test code
if __name__ == '__main__':
    source = "/media/sagar/New Volume/everything/job/Seneca/data/making_vid/clips1/*"
    output_vid_name = '/media/sagar/New Volume/everything/job/Seneca/data/making_vid/vids/clip1.avi'
    frame_to_vids(source,output_vid_name)
