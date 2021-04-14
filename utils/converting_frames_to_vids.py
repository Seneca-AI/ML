"""
sample CLI:
1. cd utils
2. python3 converting_frames_to_vids.py \
    --source_images [path/to/directory/containing/source/images] \
    --output_vid [path/to/output/video]
Code Description
Making vid from images
"""

import argparse
import glob

import cv2 # pylint: disable=import-error

def init_args():
    """
    Initialize command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--source_images',
        type=str,
        default = "../data/source_images",
        help='The path to the input images'
    )
    parser.add_argument(
        '--output_vid',
        type=str,
        default= "../frames_to_vid_out/out.avi",
        help='name and path to the output video'
    )
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
        height, width, _ = img.shape
        size = (width,height)
        img_array.append(img)

    out = cv2.VideoWriter(output_vid_name,cv2.VideoWriter_fourcc(*'DIVX'), 30, size)

    for img in img_array:
        out.write(img)
    out.release()


if __name__ == '__main__':
    args = init_args()
    frame_to_vids(source = args.source_images,output_vid_name = args.output_vid)
