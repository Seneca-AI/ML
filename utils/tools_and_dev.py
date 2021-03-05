#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 17:06:18 2021

@author: sagar

# For reading the images and converting them all to 256,512 as the binary masks are of this size

"""

#%% imports

import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob


#%% for reading and resizing images, Images are now available in the folder. 
"""
"""
source = glob.glob("/media/sagar/New Volume/everything/job/Seneca/detecting_lane_changes/images/images/*")

for i in source:
    a = cv2.imread(i)
    image = cv2.resize(a, (512,256), interpolation = cv2.INTER_AREA)
    name = i.split("/")[-1]
    cv2.imwrite("/media/sagar/New Volume/everything/job/Seneca/detecting_lane_changes/images/resized_images/"+ name,image)
    
#%% Experimentation with the lanes and bounding box
"""
Two methods are there for the same. 
1. Have the coordinates noted and check for the lane points in the bounding box
2. Make a mask of the bounding box and multiply that with the binary mask image. 
Must resize the image for the same into 256,512
"""

#%% For creating flip images. No need to run.

# read image
straight_mask = cv2.imread("/media/sagar/New Volume/everything/job/Seneca/detecting_lane_changes/images/binary_masks/0131-1_1020_8_binary.jpg",0)
image = cv2.flip(straight_mask, 1)
cv2.imwrite("/media/sagar/New Volume/everything/job/Seneca/detecting_lane_changes/images/binary_masks/0131-1_1020_8_binary_flipped.jpg", image)
plt.figure('straight_mask_image')
plt.imshow(straight_mask)
plt.show()

curved_mask = cv2.imread("/media/sagar/New Volume/everything/job/Seneca/detecting_lane_changes/images/binary_masks/0313-1_60_1_binary.jpg",0)
image = cv2.flip(curved_mask, 1)
cv2.imwrite("/media/sagar/New Volume/everything/job/Seneca/detecting_lane_changes/images/binary_masks/0313-1_60_1_binary_flipped.jpg", image)
plt.figure('curved_mask_image')
plt.imshow(curved_mask)
plt.show()

cv2.imshow("s", curved_mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

#%% variables rectangles measurement as to see at which point is the overlap happening (FOr demo purpose only)
source_binary = "/media/sagar/New Volume/everything/job/Seneca/detecting_lane_changes/images/binary_masks/*"
for i in glob.glob(source_binary):
    img = cv2.imread(i,0)
    X1 = int(img.shape[1]*1/4)+2
    X2 = int(img.shape[1]*3/4)
    Y1 = 211
    Y2 = len(img)
    start_point = (X1,Y1)
    end_point = (X2,Y2)
    thickness = 2
    color = (255,255,0)
    # image_rectangle = cv2.rectangle(img, start_point, end_point, color, thickness=1)
    # cv2.imshow("image", image_rectangle)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    cropped_area = img[Y1:Y2,X1:X2]
    unique_array = np.unique(cropped_area)
    element = [250,251,252,253,254,255]
    existing = np.isin(element, unique_array)
    print(i)
    for j in existing:
        #print(i)
        if j == False:
            print("lane change did not happen")
        elif j == True:
            print("lane change has happened")
            break

#%% deciding if the lanes exist in the area after cropping the area
source_binary = "/media/sagar/New Volume/everything/job/Seneca/data/making_vid/binary_results/*"
import pandas as pd
names = []
lane_change = []
for i in sorted(glob.glob(source_binary)):
    s = 0
    img = cv2.imread(i,0)
    img = cv2.resize(img, (512,257), interpolation = cv2.INTER_AREA)
    cv2.imshow("img", img)
    cv2.waitKey()
    cv2.destroyAllWindows()
    break
    
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
dict = {'name_of_img': names, 'lane change (0/1)': lane_change}   
   
df = pd.DataFrame(dict)  
    
# saving the dataframe  
df.to_csv('/media/sagar/New Volume/everything/job/Seneca/detecting_lane_changes/github/ML/Image_names_and_lane_change_status.csv')  
    
            
            
 



