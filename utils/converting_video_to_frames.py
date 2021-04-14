"""
sample CLI: 
1. cd utils
2. python3 converting_video_to_frames.py --source_vid /media/sagar/"New Volume"/everything/job/Seneca/data/making_vid/vids/clip2.avi --output_images /media/sagar/"New Volume"/everything/job/Seneca/data/making_vid/frame_extraction/
Code Description
Outputs the extracted frames from a given video file and outputs them to a specified directory.
"""
import cv2
import time
import os
import argparse

def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source_vid', type=str, default = "/media/sagar/New Volume/everything/job/Seneca/data/making_vid/vids/clip2.avi",help='The path to the input vid')
    parser.add_argument('--output_images', type=str, default= "/media/sagar/New Volume/everything/job/Seneca/data/making_vid/frame_extraction/",help='path to output frames of the vid')
    return parser.parse_args()

def video_to_frames(input_loc, output_loc):
    """
    Function to extract frames from input video file
    and save them as separate frames in an output directory.
    Args:
        input_loc: Input video file.
        output_loc: Output directory to save the frames.
    Returns:
        None
    """
    # Warnings and errors
    if not os.path.exists(input_loc):
        raise ValueError("The required vid is not present. Please recheck the input vid source.")
    
    #Function starts
    if not os.path.exists(output_loc):
        try:
            os.mkdir(output_loc)
        except OSError:
            pass
    time_start = time.time()
    video_capture = cv2.VideoCapture(input_loc)
    frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    print ("Number of frames: ", frame_count)
    count = 0
    print ("Converting video..\n")
    while video_capture.isOpened():
        ret, frame = video_capture.read()
        cv2.imwrite(output_loc + "/%#05d.jpg" % (count+1), frame)
        count = count + 1
        if (count > (frame_count-1)):
            time_end = time.time()
            video_capture.release()
            print ("Done extracting frames.\n%d frames extracted" % count)
            print ("It took %d seconds for conversion." % (time_end-time_start))
            break

if __name__=="__main__":
    args = init_args()
    video_to_frames(input_loc = args.source_vid, output_loc = args.output_images)