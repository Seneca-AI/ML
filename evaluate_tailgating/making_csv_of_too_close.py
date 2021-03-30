"""
CLI 
python3 Making_csv_of_too_close.py --source_images clip4/*.jpg --source_labels labels --CSV_destination Image_names_and_too_close_status.csv
code for overlapping the BBOX with image and finding if they are too close or not.
We have taken classes of 2 (car), 5 (bus), 7 (truck)
"""
import cv2
import numpy as np
import glob
import pandas as pd
import argparse

def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source_images', type=str, default = '/media/sagar/New Volume/everything/job/Seneca/data/making_vid/tailgatin_data/too_close/images/*.jpg',help='The path to the input images ')
    parser.add_argument('--source_labels', type=str, default = '/media/sagar/New Volume/everything/job/Seneca/data/making_vid/tailgatin_data/too_close/labels/',help='Path to the labels of the BBOX during the yolov5 evaluation')
    parser.add_argument('--CSV_destination', type=str, default= 'Image_names_and_too_close_status.csv',help='path to where you wish to save the csv file')
    return parser.parse_args()

def making_csv_of_too_close(source_images, source_labels, CSV_destination):
    """
    

    Parameters
    ----------
    source_images : str
        DESCRIPTION: Path to the input images
    source_labels : str
        DESCRIPTION: path to the output images
    CSV_destination : str
        DESCRIPTION: Path of where you wish to save the csv file.

    Returns
    -------
    Generates a csv with all the frame names along with the values of too close or not. 1 is given if the vehicle is
    too close. 0 is written if no vehicle is found too close to the vehicle in question.  

    """
    
    # from experimentation setting the coordinates of the bounding box in the form of x1,y1,x2,y2
    box_coordinates = np.array([560,230,730,390])
    
    #We have taken classes of 2 (car), 5 (bus), 7 (truck)
    classes_taken = np.array([2,5,7])
    
    names = []
    too_close = []
    for i in sorted(glob.glob(source_images)):
        img = cv2.imread(i)
        height_img,width_img = img.shape[0], img.shape[1]
        label = source_labels +"labels/" +i.split("/")[-1].split(".")[0] + ".txt"
        dataframe = pd.read_csv(label, sep=" ", header = None)
        names.append(i.split("/")[-1])
        
        #condition for closeness
        found_too_close = 0
        
        for j in range(len(dataframe)):
            
            class_value = dataframe._get_value(j,0)
            if class_value in classes_taken:
                x_centre_vehicle = dataframe._get_value(j,1)
                y_centre_vehicle = dataframe._get_value(j,2)
                width_vehicle = dataframe._get_value(j,3)
                height_vehicle = dataframe._get_value(j,4)
                
                x1 = int((x_centre_vehicle - width_vehicle/2) *width_img)
                y1 = int((y_centre_vehicle - height_vehicle/2) *height_img)
                
                x2 = int((x_centre_vehicle + width_vehicle/2) * width_img)
                y2 = int((y_centre_vehicle + height_vehicle/2) *height_img)
                
                if x1 < box_coordinates[0] and y1 < box_coordinates[1] and x2 > box_coordinates[2] and y2 > box_coordinates[3]:
                    found_too_close = 1
                    break
                else:
                    found_too_close = 0
            if found_too_close==1:
                break
            else:
                continue
        too_close.append(found_too_close)
        
    dict = {'name_of_img': names, 'too close (0/1)': too_close}   
    dataframe = pd.DataFrame(dict) 
    dataframe.to_csv(CSV_destination)
    
    #TODO Add exception and error handling

if __name__ == '__main__':
    args = init_args()
    making_csv_of_too_close(source_images = args.source_images, source_labels = args.source_labels, CSV_destination= args.CSV_destination)