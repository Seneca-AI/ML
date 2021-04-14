"""
Sample CLI:
python3 making_concurrent_frames_Tusimple.py --source_dataset {path/to/inpute/dataset} \
     --output_images {path/to/output/images]}
Code Description
The code is used for renaming the images if they are in given (in the function) incorrect format.
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
        '--source_dataset',
        type=str,
        default = "../data/making_vid/frames2/*/*",help='The path to the input dataset'
    )
    parser.add_argument(
        '--output_images',
        type=str,
        default= "../data/making_vid/delete_if_seen/",
        help='path to where you wish to save the frames'
    )
    return parser.parse_args()

# TODO(Luca409): figure out these things
#       -   why this function has "if" in its name, but has no conditionals
#       -   why this shouldn't be done in place (using same directory path)
#       -   why this needs to be done at all (rename if for a specific data source)
def renaming_padding_if_in_folder_names(source, dest):
    """

    Parameters
    ----------
    source : string
        The dataset to rename.
    dest : string
        Where the renamed files should be stored, (if there are any?).


    Returns
    -------
    hi : list
        It is a list of all the images that we just sorted and renamed

    """
    names = []
    lengths = []
    for i in glob.glob(source):
        img = cv2.imread(i)

        name = str(int(i.split("/")[-2])+int((i.split("/")[-1]).split(".")[0]))
        length = len(name)
        lengths.append(length)
    maximum_name_length = max(lengths)

    for i in glob.glob(source):
        img = cv2.imread(i)
        name = str(int(i.split("/")[-2])+int((i.split("/")[-1]).split(".")[0]))
        name_len = len(name)
        zeros_length = maximum_name_length - name_len
        new_name = name.zfill(zeros_length + len(name))
        names.append(new_name)
        cv2.imwrite(dest + new_name + ".jpg", img)
    return sorted(names)

if __name__ == '__main__':
    args = init_args()
    renaming_padding_if_in_folder_names(source = args.source_dataset,dest = args.output_images)
