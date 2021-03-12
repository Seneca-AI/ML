"""
Making vid from images
"""

import cv2
import numpy as np
import glob
import argparse

def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source_images', type=str, default = "/media/sagar/New Volume/everything/job/Seneca/data/making_vid/clips1/*",help='The path to the input images')
    parser.add_argument('--output_vid', type=str, default= "/media/sagar/New Volume/everything/job/Seneca/data/making_vid/vids/clip1.avi",help='name and path to the output video')
    return parser.parse_args()

def frame_to_vids(source,output_vid_name):
    """
    
    Parameters
    ----------
    source : str
        Path to the input images 
    output_vid_name : avi vid
        name and path to the output video

    Returns
    -------
    Makes the video of the input frames.
    Function does not return any output

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
    

if __name__ == '__main__':
    args = init_args()
    frame_to_vids(source = args.source_images,output_vid_name = args.output_vid)
