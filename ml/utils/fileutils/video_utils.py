"""
video_utils handles operations around manipulating video data before ML processing
"""

# TODO(lucaloncar): re-assess the validity of the code in this file

import glob
import os

import cv2

from api.exceptions import InvalidInputError

def frames_to_vid(path_to_input_frames_dir: str, path_to_output_video: str):
    """
    frames_to_vid stitches together the given frames into a video and stores
    it at path_to_output_video

    Params:
        path_to_frames_dir string: path to the input images directory
        path_to_output_video string

    Returns:
        None
    """
    if path_to_input_frames_dir[-1] == '*' or path_to_input_frames_dir[-1] == '/':
        raise InvalidInputError("path_to_input_frames_dir must not end in * or /")

    if not os.path.isdir(path_to_input_frames_dir):
        raise FileNotFoundError(
            "path_to_input_frames_dir {0} does not exist".format(path_to_input_frames_dir))

    path_to_input_frames_dir = path_to_input_frames_dir + "/*"

    img_array = []
    for filename in sorted(glob.glob(path_to_input_frames_dir)):
        img = cv2.imread(filename)
        height, width, _ = img.shape
        size = (width,height)
        img_array.append(img)

    out = cv2.VideoWriter(path_to_output_video, cv2.VideoWriter_fourcc(*'mp4v'), 30, size)

    for img in img_array:
        out.write(img)
    out.release()


def vid_to_frames(path_to_input_vid: str, path_to_output_frames_dir: str):
    """
    vid_to_frames splits the given video into individual frames
    and stores them in the path_to_output_frames_dir

    Params:
        path_to_input_vid string: path to the input video to split into frames
        path_to_output_frames_dir string: path to the directory where the output
                                          frames will be written to

    Returns:
        None
    """
    if not os.path.isdir(path_to_output_frames_dir):
        os.mkdir(path_to_output_frames_dir)

    if not os.path.isfile(path_to_input_vid):
        raise FileNotFoundError("path_to_input_vid {0} does not exist".format(path_to_input_vid))

    cap = cv2.VideoCapture(path_to_input_vid)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    count = 0
    while cap.isOpened():
        _, frame = cap.read()
        cv2.imwrite(path_to_output_frames_dir + "/%#05d.jpg" % (count), frame)
        count = count + 1
        if count > (frame_count - 1):
            cap.release()
            break
