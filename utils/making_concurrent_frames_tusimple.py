"""
Sample CLI:
python3 making_concurrent_frames_Tusimple.py --source_dataset /media/sagar/"New Volume"/everything/job/Seneca/data/making_vid/frames2/*/* --output_images /media/sagar/"New Volume"/everything/job/Seneca/data/making_vid/delete_if_seen/
Code Description
The code is used for renaming the images if they are in given (in the function) incorrect format.
"""

import cv2
import glob
import os
import numpy as np
import argparse
def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source_dataset', type=str, default = "/media/sagar/New Volume/everything/job/Seneca/data/making_vid/frames2/*/",help='The path to the input dataset')
    parser.add_argument('--output_images', type=str, default= "/media/sagar/New Volume/everything/job/Seneca/data/making_vid/delete_if_seen/",help='path to where you wish to save the frames')
    return parser.parse_args()

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
    images: save images with renamed and in the indicated directories, 
    all the images have 0s appended in the front for easier sorting
    renamed_img_list : list
        It is a list of all the images that we just sorted and renamed

    """
    names = []
    lengths = []
    for i in glob.glob(Source):
        img = cv2.imread(i)
        if img is None:
            raise ValueError("Input images are either missing or None. Please check the source folder.")
        name = str(int(i.split("/")[-2])+int((i.split("/")[-1]).split(".")[0]))
        length = len(name)
        lengths.append(length)
    maximum_name_length = max(lengths)
    
    for i in glob.glob(Source):
        img = cv2.imread(i)
        name = str(int(i.split("/")[-2])+int((i.split("/")[-1]).split(".")[0]))
        name_len = len(name)
        zeros_length = maximum_name_length - name_len
        new_name = name.zfill(zeros_length + len(name))
        names.append(new_name)
        cv2.imwrite(Dest + new_name + ".jpg", img)
        read_img = cv2.imread(Dest + new_name + ".jpg")
        if read_img is None:
            raise ValueError("""Output folder or the images being made are corrupt or NoneType.
                             Please check the function and output folder""")
    renamed_img_list = sorted(names)
    return renamed_img_list

if __name__ == '__main__':
    args = init_args()
    renaming_padding_if_in_folder_names(Source = args.source_dataset,Dest = args.output_images)