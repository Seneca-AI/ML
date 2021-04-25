"""
The lane_chaning module is the main entry point for converting
a raw video to its lane changing data.
"""

from api.type import processed_pb2

def mark_lane_changes(path_to_video: str) -> processed_pb2.LaneChangesForVideo:
    # pylint: disable=unused-argument
    """
    Implements main logic for marking lane changes.
    Params:
        path_to_video string: the path to the input video
    Returns:
        processed_pb2.LaneChangesForVideo: filled out lane changes for the video
    """
    # TODO(absagargupta): implement this
    lane_changes_for_video = processed_pb2.LaneChangesForVideo()
    lane_changes_for_video.num_frames = 10

    for i in range(lane_changes_for_video.num_frames):
        lnff = processed_pb2.LaneChangesForVideo.LaneChangeForFrame()
        lnff.frame_index = i
        lnff.lane_change = (i % 2) == 0
        lane_changes_for_video.lane_change_for_frame.append(lnff)

    return lane_changes_for_video
