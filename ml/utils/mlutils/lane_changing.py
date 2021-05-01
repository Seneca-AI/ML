""" lane_changing implements all basic functions related to lane_changing. """

from quarantined.lane_detection.tools.evaluate_lanenet_on_tusimple import eval_lanenet

def generate_lane_masks(input_frames_dir: str, output_masks_dir: str):
    """
    generate_lane_masks generates a mask over lanes for each image in input_frames_dir
    and stores the results in output_masks_dir

    Params:
        input_frames_dir str: the path to the input frames
        output_masks_dir str: the path where output masks will be stored

    Returns:
        None
    """
    eval_lanenet(
        input_frames_dir,
        "quarantined/lane_detection/trained_model/tusimple_lanenet.ckpt",
        output_masks_dir
        )
