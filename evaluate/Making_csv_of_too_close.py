"""
CLI 
python3 Making_csv_of_too_close.py --source_images clip4/*.jpg --source_labels labels --CSV_destination Image_names_and_too_close_status.csv
code for overlapping the BBOX with image
We have taken classes of 2 (car), 5 (bus), 7 (truck)
"""
import cv2
import numpy as np
import glob
import pandas as pd
import argparse

def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source_images', type=str, default = "/media/sagar/New Volume/everything/job/Seneca/data/making_vid/tailgatin_data/clip4/*.jpg",help='The path to the input images ')
    parser.add_argument('--source_labels', type=str, default = "/media/sagar/New Volume/everything/job/Seneca/data/making_vid/tailgatin_data/clip4/labels",help='Path to the labels of the BBOX during the yolov5 evaluation')
    parser.add_argument('--CSV_destination', type=str, default= 'Image_names_and_too_close_status.csv',help='path to where you wish to save the csv file')
    return parser.parse_args()

def Drawing_BBOX_on_vehicles(source_images, source_labels, CSV_destination):
    box2 = np.array([560,230,730,390])
    classes_taken = np.array([2,5,7])
    names = []
    too_close = []
    for i in sorted(glob.glob(source_images)):
        #print(i)
        img = cv2.imread(i)
        label = source_labels + "/" + i.split("/")[-1].split(".")[0] + ".txt"
        df = pd.read_csv(label, sep=" ", header = None)
        names.append(i.split("/")[-1])
        s = 0
        for j in range(len(df)):
            #print(len(df))
            class_value = df._get_value(j,0)
            if class_value in classes_taken:
                x_centre = df._get_value(j,1)
                y_centre = df._get_value(j,2)
                width = df._get_value(j,3)
                height = df._get_value(j,4)
                
                ht,wd,_ = img.shape[0], img.shape[1], img.shape[2]
                
                x1 = int((x_centre - width/2) *wd)
                y1 = int((y_centre - height/2) *ht)
                
                x2 = int((x_centre + width/2) * wd)
                y2 = int((y_centre + height/2) *ht)
                #print(x1,y1,x2,y2)
                if x1 < box2[0] and y1 < box2[1] and x2 > box2[2] and y2 > box2[3]:
                    s = 1
                    break
                else:
                    s = 0
            if s==1:
                break
            else:
                continue
        too_close.append(s)
    dict = {'name_of_img': names, 'too close (0/1)': too_close}   
    df = pd.DataFrame(dict) 
    df.to_csv(CSV_destination)

if __name__ == '__main__':
    args = init_args()
    Drawing_BBOX_on_vehicles(source_images = args.source_images, source_labels = args.source_labels, CSV_destination= args.CSV_destination)



