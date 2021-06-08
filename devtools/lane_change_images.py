from ml.utils.mlutils.lane_changing import generate_lane_masks


path_to_frames='data/temp/1623127632998/frames'
path_to_masks='tmp/labeled'

generate_lane_masks(path_to_frames, path_to_masks)