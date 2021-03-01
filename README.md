# ML

This code is used for taking up a trained model and using the model for inference on a set of frames. 

1. Install the dependencies as given(can be in a conda environment, or a docker)
2. Run evaluate_vid_on_lanenet.py by giving the following arguments: 
 - image dir (should contain all the images that need to be inferred)
 - weights_path (should contain the .ckpt file of the lanenet)
 - save_dir (the path where u want your images annotated along with the lanes on top of them)
 - save_dir_binary (the path where you wish to store the annotation binary masks)
3. In the code_and_mark_lane_changes.py put source of the binary files which was given in the above step 2. The last line saves the frames and the lane change w.r.t. each of the frame.
