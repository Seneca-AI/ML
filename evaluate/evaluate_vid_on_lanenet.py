"""
sample CLI
python3 evalualte_vid_on_lanenet.py --image_dir ./clips --weights_path ./tusimple_lanenet.ckpt --save_dir ./results2 --save_dir_binary ./binary_results2
Evaluate lanenet model on any vid
"""
import argparse
import glob
import os
import os.path as ops
import time

import cv2
import numpy as np
import tensorflow as tf
import tqdm
import sys
sys.path.append("../")

from source.lanenet_model import lanenet
from source.lanenet_model import lanenet_postprocess
from source.local_utils.config_utils import parse_config_utils
from source.local_utils.log_util import init_logger

CFG = parse_config_utils.lanenet_cfg
LOG = init_logger.get_logger(log_file_name_prefix='lanenet_eval_vid')

def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_dir', type=str, default = "/media/sagar/New Volume/everything/job/Seneca/data/making_vid/clips2/clips",help='The source tusimple lane test data dir')
    parser.add_argument('--weights_path', type=str, default= "/media/sagar/New Volume/everything/job/Seneca/weights/BiseNetV2_LaneNet_Tusimple_Model_Weights/tusimple_lanenet.ckpt",help='The model weights path')
    parser.add_argument('--save_dir', type=str,default = "/media/sagar/New Volume/everything/job/Seneca/data/making_vid/results2", help='The test output save root dir')
    parser.add_argument('--save_dir_binary', type=str,default = "/media/sagar/New Volume/everything/job/Seneca/data/making_vid/binary_results2", help='The test output save root dir')
    return parser.parse_args()

def evaluate_vid_on_lanenet(src_dir, weights_path, save_dir,save_dir_binary):
    """
    This functions takes the images from the image_dir and makes a binary mask of the lanes
    over all the images. These lane binary images can be used for further computation.

    Parameters
    ----------
    src_dir : string
        DESCRIPTION path of the frames
    weights_path : string
        DESCRIPTION. trained model weight .ckpt file
    save_dir : string
        DESCRIPTION: path of the folder where the results are to be saved
    save_dir_binary : TYPE
        DESCRIPTION: path to folder where the binary results are to besaved

    Returns
    -------
    Images with lanes marked on them in the save_dir folder and binary results in the save_dir_binary folder

    """
    assert ops.exists(src_dir), '{:s} not exist'.format(src_dir)

    os.makedirs(save_dir, exist_ok=True)
    
    assert ops.exists(save_dir_binary), '{:s} not exist'.format(save_dir_binary)

    os.makedirs(save_dir_binary, exist_ok=True)
    
    if os.path.exists(src_dir):
        pass
    else:
        raise ValueError("The required input images are not present. Please recheck the input image source")
    check_img = glob.glob(src_dir + "/*")
    for i in check_img:
        if i.split("/")[-1].split(".")[1] == "jpg":
            pass
        else:
            raise ValueError("Please check the input source. They might not have jpg files")
    
    if os.path.exists(weights_path + ".index"):
        pass
    else:
        raise ValueError("The required weight files are not present at the given directory. Please recheck the weights path")
        
    input_tensor = tf.placeholder(dtype=tf.float32, shape=[1, 256, 512, 3], name='input_tensor')

    net = lanenet.LaneNet(phase='test', cfg=CFG)
    binary_seg_ret, instance_seg_ret = net.inference(input_tensor=input_tensor, name='LaneNet')

    postprocessor = lanenet_postprocess.LaneNetPostProcessor(cfg=CFG)

    saver = tf.train.Saver()

    # Set sess configuration
    sess_config = tf.ConfigProto()
    sess_config.gpu_options.per_process_gpu_memory_fraction = CFG.GPU.GPU_MEMORY_FRACTION
    sess_config.gpu_options.allow_growth = CFG.GPU.TF_ALLOW_GROWTH
    sess_config.gpu_options.allocator_type = 'BFC'

    sess = tf.Session(config=sess_config)

    with sess.as_default():

        saver.restore(sess=sess, save_path=weights_path)

        image_list = glob.glob('{:s}/**/*.jpg'.format(src_dir), recursive=True)
        avg_time_cost = []
        for index, image_path in tqdm.tqdm(enumerate(image_list), total=len(image_list)):

            image = cv2.imread(image_path, cv2.IMREAD_COLOR)
            image_vis = image
            size = (512, 256)
            image = cv2.resize(image, size, interpolation=cv2.INTER_LINEAR)
            image = image / 127.5 - 1.0

            t_start = time.time()
            binary_seg_image, instance_seg_image = sess.run(
                [binary_seg_ret, instance_seg_ret],
                feed_dict={input_tensor: [image]}
            )
            avg_time_cost.append(time.time() - t_start)

            postprocess_result = postprocessor.postprocess(
                binary_seg_result=binary_seg_image[0],
                instance_seg_result=instance_seg_image[0],
                source_image=image_vis
            )

            if index % 100 == 0:
                LOG.info('Mean inference time every single image: {:.5f}s'.format(np.mean(avg_time_cost)))
                avg_time_cost.clear()

            input_image_dir = ops.split(image_path.split('clips')[1])[0][1:]
            input_image_name = ops.split(image_path)[1]
            output_image_dir = ops.join(save_dir, input_image_dir)
            os.makedirs(output_image_dir, exist_ok=True)
            output_image_path = ops.join(output_image_dir, input_image_name)
            output_bin_image_dir = ops.join(save_dir_binary, input_image_name)
            binary_seg_result=binary_seg_image[0]
            if ops.exists(output_bin_image_dir):
                continue
            
            cv2.imwrite(output_bin_image_dir,binary_seg_result*255)

            if ops.exists(output_image_path):
                continue
            
            cv2.imwrite(output_image_path, postprocess_result['source_image'])

if __name__ == '__main__':
    args = init_args()
    evaluate_vid_on_lanenet(
        src_dir=args.image_dir,
        weights_path=args.weights_path,
        save_dir=args.save_dir,
        save_dir_binary = args.save_dir_binary
    )
