"""
The object_detection module identifies objects in an image, and gives their size and location.
"""

import os

import cv2

from quarantined.object_detection.tool.torch_utils import do_detect
from quarantined.object_detection.tool.darknet2pytorch import Darknet


# pylint: disable=too-few-public-methods
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

    def classify_image(self, path_to_img_file: str):
        """
        classify_image takes the image and runs it through the model to produce bounding boxes of
        objects
        Params:
            path_to_img_file string: the path to the input image
        Returns:
            boxes: ? TOOD(lucaloncar): document
        """
        if not os.path.exists(path_to_img_file):
            raise FileNotFoundError(path_to_img_file)

        img = cv2.imread(path_to_img_file)
        sized = cv2.resize(img, (self.model.width, self.model.height))
        sized = cv2.cvtColor(sized, cv2.COLOR_BGR2RGB)


        for _ in range(2):
            boxes = do_detect(self.model, sized, 0.4, 0.6, True)

        return boxes
