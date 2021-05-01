"""
The lane_chaning module is the main entry point for converting
a raw video to its lane changing data.
"""
import os
import shutil
import time

from api.constants import VIDEO_TMP_FILE_LOCATION
from api.type import processed_pb2
from ml.utils.fileutils.video_utils import vid_to_frames
from ml.utils.mlutils.lane_changing import generate_lane_masks

def get_lane_changes_for_video(path_to_video: str) -> processed_pb2.LaneChangesForVideo:
    # pylint: disable=unused-argument
    """
    get_lane_changes_for_video implements main logic for marking lane changes.
    Params:
        path_to_video string: the path to the input video
    Returns:
        processed_pb2.LaneChangesForVideo: filled out lane changes for the video
    """
    frames_dir_name = "frames"
    masks_dir_name = "masks"
    current_millis_str = str(time.time() * 1000)
    temp_dir = os.path.join(VIDEO_TMP_FILE_LOCATION, current_millis_str)
    os.mkdir(temp_dir)

    # Split video into frames and store in a temp directory.
    frames_temp_dir = os.path.join(temp_dir, frames_dir_name)
    os.mkdir(frames_temp_dir)
    vid_to_frames(path_to_video, frames_temp_dir)

    # Create binary mask over images.
    masks_temp_dir = os.path.join(temp_dir, masks_dir_name)
    os.mkdir(masks_temp_dir)
    generate_lane_masks(frames_temp_dir, masks_temp_dir)

    # TODO(lucaloncar): infer lane changign using masks

    shutil.rmtree(temp_dir)

    lane_changes_for_video = processed_pb2.LaneChangesForVideo()
    lane_changes_for_video.num_frames = 10

    for i in range(lane_changes_for_video.num_frames):
        lnff = processed_pb2.LaneChangesForVideo.LaneChangeForFrame()
        lnff.frame_index = i
        lnff.lane_change = (i % 2) == 0
        lane_changes_for_video.lane_change_for_frame.append(lnff)

    return lane_changes_for_video
