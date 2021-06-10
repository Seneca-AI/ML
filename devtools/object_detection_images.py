
import os
import shutil
import time

import cv2

from api.constants import TMP_FILE_LOCATION
from ml.utils.fileutils.video_utils import vid_to_frames
from quarantined.object_detection.tool.darknet2pytorch import Darknet
from quarantined.object_detection.tool.torch_utils import do_detect
from quarantined.object_detection.tool.utils import plot_boxes_cv2


path_to_frames='data/temp/1623127632998/frames'
path_to_frames=None

def should_include(bounding_box):
    x_lower = bounding_box[0]
    y_lower = bounding_box[1]
    x_upper = bounding_box[2]
    y_upper = bounding_box[3]
    confidence = bounding_box[4]
    label = bounding_box[6]

    # Is out of bounds.
    if x_lower < 0.25 or x_upper < 0.75:
        return False

    # Is low confidence.
    if confidence < 0.5:
        return False

    # Is not a car or a truck.
    if label != 2 and label != 7:
        return False

    width = x_upper - x_lower
    height = y_upper - y_lower

    # 1 = perfect square
    squareness = height/width

    if abs(1 - squareness) > 0.2:
        return False

    return True


# Split video into images.
path_to_video = "tmp/four.mp4"
frames_dir = ''

if path_to_frames is None: 
    frames_dir_name = "frames"
    current_millis_str = str(round(time.time() * 1000))
    temp_dir = os.path.join(TMP_FILE_LOCATION, current_millis_str)
    frames_dir = os.path.join(temp_dir, frames_dir_name)
    os.mkdir(temp_dir)
    
try:

    if path_to_frames is None:
        os.mkdir(frames_dir)
        print("Splitting video into frames...")
        vid_to_frames(path_to_video, frames_dir)
        print("Finished splitting video into frames")
    else:
        frames_dir = path_to_frames

    filenames = []
    for file in os.listdir(frames_dir):
        filename = os.fsdecode(file)
        filenames.append(filename)

    destination_directory = 'tmp/labeled'

    # Init model.
    cfgfile = 'config/ml_config/yolov4x-mish.cfg'
    weightfile = 'config/ml_config/yolov4x-mish.weights'
    m = Darknet(cfgfile)

    m.print_network()
    m.load_weights(weightfile)
    print('Loading weights from %s... Done!' % (weightfile))

    m.cuda()

    print('frames_dir: ' + frames_dir)
    for fname in filenames:
        full_fname = os.path.join(frames_dir, fname)

        img = cv2.imread(full_fname)
        sized = cv2.resize(img, (m.width, m.height))
        sized = cv2.cvtColor(sized, cv2.COLOR_BGR2RGB)

        boxes = do_detect(m, sized, 0.4, 0.6, None, True)

        plot_boxes_cv2(img, boxes[0], savename=os.path.join(destination_directory, fname), class_names=None)
finally:
    pass
    # shutil.rmtree(temp_dir)