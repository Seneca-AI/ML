"""
sample CLI:
1. cd utils
2. python3 converting_video_to_frames.py --source_vid {path/to/video} \
    --output_images {path/to/output/directory}
Code Description
Making frames from video
"""

import argparse
import os
import time

import cv2 # pylint: disable=import-error

def init_args():
    """
    Initialize command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--source_vid',
        type=str,
        default = "../videos/video_to_frames_in.avi",
        help='The path to the input vid'
    )
    parser.add_argument(
        '--output_images',
        type=str,
        default= "../data/output_images",
        help='path to output frames of the vid'
    )
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
    try:
        os.mkdir(output_loc)
    except OSError:
        pass

    time_start = time.time()
    cap = cv2.VideoCapture(input_loc)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    print ("Number of frames: ", frame_count)
    count = 0
    print ("Converting video..\n")
    while cap.isOpened():
        _, frame = cap.read()
        cv2.imwrite(output_loc + "/%#05d.jpg" % (count+1), frame)
        count = count + 1
        if count > (frame_count-1):
            time_end = time.time()
            cap.release()
            print ("Done extracting frames.\n%d frames extracted" % count)
            print ("It took %d seconds for conversion." % (time_end-time_start))
            break

if __name__=="__main__":
    args = init_args()
    video_to_frames(input_loc = args.source_vid, output_loc = args.output_images)
