"""
The lane_chaning module is the main entry point for converting
a raw video to its lane changing data.
"""
import os
import shutil
import time

from api.constants import VIDEO_TMP_FILE_LOCATION
from api.type import processed_pb2

def get_lane_changes_for_video(path_to_video: str) -> processed_pb2.LaneChangesForVideo:
    """
    get_lane_changes_for_video implements main logic for marking lane changes.
    Params:
        path_to_video string: the path to the input video
    Returns:
        processed_pb2.LaneChangesForVideo: filled out lane changes for the video
    """
    if not os.path.exists(path_to_video):
        raise FileNotFoundError(path_to_video)

    # Create directories to stage files.
    frames_dir_name = "frames"
    masks_dir_name = "masks"
    current_millis_str = str(round(time.time() * 1000))
    temp_dir = os.path.join(VIDEO_TMP_FILE_LOCATION, current_millis_str)
    frames_dir = os.path.join(temp_dir, frames_dir_name)
    masks_dir = os.path.join(temp_dir, masks_dir_name)
    os.mkdir(temp_dir)
    os.mkdir(frames_dir)
    os.mkdir(masks_dir)

    # TODO(lucaloncar): infer lane changing using masks

    shutil.rmtree(temp_dir)

    lane_changes_for_video = processed_pb2.LaneChangesForVideo()
    lane_changes_for_video.num_frames = 10

    for i in range(lane_changes_for_video.num_frames):
        lnff = processed_pb2.LaneChangesForVideo.LaneChangeForFrame()
        lnff.frame_index = i
        lnff.lane_change = (i % 2) == 0
        lane_changes_for_video.lane_change_for_frame.append(lnff)

    return lane_changes_for_video
