"""
The object_detection module identifies objects in an image, and gives their size and location.
"""

import os
import shutil
import time

import cv2

from api.constants import TMP_FILE_LOCATION
from api.type import processed_pb2
from ml.utils.fileutils.video_utils import vid_to_frames
from quarantined.object_detection.tool.darknet2pytorch import Darknet
from quarantined.object_detection.tool.torch_utils import do_detect


class ObjectDetector:
    """
    ObjectDetector initializes the model.
    """

    def __init__(self, cfg_file_path: str, weight_file_path: str):
        if not os.path.exists(cfg_file_path):
            raise FileNotFoundError(cfg_file_path)
        if not os.path.exists(weight_file_path):
            raise FileNotFoundError(weight_file_path)

        self.model = Darknet(cfg_file_path)
        self.model.cuda()
        self.model.load_weights(weight_file_path)


        self.label_mapping = {
            # car
            2: 1,
            7: 2
        }

    def classify_video(self, path_to_video: str):
        """
        classify_video takes the video, cuts it up into frames, and runs all of them
        through classify_image
        Params:
            path_to_video string: the path to the input video
        Returns:
            dict[int]processed_pb2.ObjectsInFrame: objects in the frame indexed by frame number
        """
        if not os.path.exists(path_to_video):
            raise FileNotFoundError(path_to_video)

        # Create directories to stage frames.
        frames_dir_name = "frames"
        current_millis_str = str(round(time.time() * 1000))
        temp_dir = os.path.join(TMP_FILE_LOCATION, current_millis_str)
        frames_dir = os.path.join(temp_dir, frames_dir_name)
        os.mkdir(temp_dir)
        os.mkdir(frames_dir)

        vid_to_frames(path_to_video, frames_dir)

        filenames = []
        for file in os.listdir(frames_dir):
            filename = os.fsdecode(file)
            filenames.append(filename)

        objects_in_frames = dict()
        for fname in filenames:
            object_in_frames = self.classify_image(os.path.join(frames_dir, fname))

            # Remove leading zeroes.
            fname = fname.strip("0")
            # Remove suffix.
            fname = fname.strip(".jpg")
            # But if we have an empty string it must"ve been all zeroes.
            if fname == "":
                fname = "0"

            objects_in_frames[int(fname)] = object_in_frames

        shutil.rmtree(temp_dir)

        return objects_in_frames

    def classify_image(self, path_to_image: str) -> processed_pb2.ObjectsInFrame:
        """
        classify_image takes the image and runs it through the model to produce bounding boxes of
        objects
        Params:
            path_to_image string: the path to the input image
        Returns:
            processed_pb2.ObjectsInFrame: object boxes in this frame
        """
        if not os.path.exists(path_to_image):
            raise FileNotFoundError(path_to_image)

        img = cv2.imread(path_to_image)
        sized = cv2.resize(img, (self.model.width, self.model.height))
        sized = cv2.cvtColor(sized, cv2.COLOR_BGR2RGB)

        for _ in range(2):
            boxes = do_detect(self.model, sized, 0.4, 0.6, True)

        objects_in_frame = processed_pb2.ObjectsInFrame()

        if len(boxes) != 1:
            return objects_in_frame

        for box in boxes[0]:
            # TODO(lucaloncar): log this
            if len(box) != 7:
                continue

            object_box = processed_pb2.ObjectBox()
            object_box.x_lower = box[0]
            object_box.y_lower = box[1]
            object_box.x_upper = box[2]
            object_box.y_upper = box[3]
            object_box.confidence = box[4]

            if box[6] in self.label_mapping:
                object_box.object_label = self.label_mapping[box[6]]
            else:
                object_box.object_label = 0

            objects_in_frame.object_box.append(object_box)

        return objects_in_frame
