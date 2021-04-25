"""
The following_distance module is the main entry point for converting
a raw video toits following distancedata.
"""

from api.type import processed_pb2

def mark_following_distance(path_to_video: str) -> processed_pb2.FollowingDistanceForVideo:
    # pylint: disable=unused-argument
    """
    Implements main logic for marking following distance.
    Params:
        path_to_video string: the path to the input video
    Returns:
        processed_pb2.FollowingDistanceForVideo: filled out following distance for the video
    """
    # TODO(absagargupta): implement this
    following_distance_for_video = processed_pb2.FollowingDistanceForVideo()
    following_distance_for_video.num_frames = 10

    for i in range(following_distance_for_video.num_frames):
        fdff = processed_pb2.FollowingDistanceForVideo.FollowingDistanceForFrame()
        fdff.frame_index = i
        fdff.is_too_close = (i % 2) == 0
        following_distance_for_video.following_distance_for_frame.append(fdff)

    return following_distance_for_video
