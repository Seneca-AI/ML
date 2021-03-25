"""
CLI
python3 yolov5_inference.py --weights ../source_tailgating/yolov5s.pt --source ../data/too_close/images --img-size 1280 --conf-thres 0.25 --iou-thres 0.45 --device "-1" --output_folder ../data/too_close/labels/ 
Code for getting the inference of the yolov5
"""

import argparse
import time
from pathlib import Path

import cv2
import torch
from numpy import random
import os
import sys
sys.path.append("../source_tailgating")

from models.experimental import attempt_load
from utils.datasets import LoadImages
from utils.general import check_img_size, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized


def detect(weights, source, img_size, conf_thres, iou_thres, device, save_txt, save_conf, classes, output_folder):
    
    """
    This function is used for finding the various vehicles and get their coordinates.

    Parameters
    ----------
    weights : str
        DESCRIPTION: Address of the yolo weights
    source : str
        DESCRIPTION: Address of the images
    img-size : int
        DESCRIPTION: size of the images
    conf-thres : float
        DESCRIPTION: object confidence threshold
    iou-thres : float
        DESCRIPTION: IOU threshold for NMS
    device : int
        DESCRIPTION: -1 for cpu, 0 or 1 for gpu
    save-txt : str
        DESCRIPTION: save results to *.txt
    save-conf : Bool
        DESCRIPTION: save confidences in --save-txt labels
    classes : int
        DESCRIPTION: These are the classes you wish to obtain. Leave blank for all
    output_folder : str
        DESCRIPTION: Output folder where you want to have the labels put.

    Returns
    -------
    Saves labels of all classes and images along with detected objects

    """
    
    source, weights, save_txt, imgsz = source, weights, save_txt, img_size

    # Directories
    save_dir =Path(output_folder)
    (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir
    
    save_dir_imgs = str(save_dir) + "/images"
    if os.path.exists(save_dir_imgs):
        pass
    else:
        os.mkdir(save_dir_imgs)
        
    # Initialize
    set_logging()
    device = select_device(device)
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(imgsz, s=stride)  # check img_size
    if half:
        model.half()  # to FP16

    # Second-stage classifier
    classify = False
    if classify:
        modelc = load_classifier(name='resnet101', n=2)  # initialize
        modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=device)['model']).to(device).eval()

    # Set Dataloader
    vid_path, vid_writer = None, None
    save_img = True
    dataset = LoadImages(source, img_size=imgsz, stride=stride)

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    t0 = time.time()
    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        t1 = time_synchronized()
        pred = model(img, augment=False)[0]

        # Apply NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes=classes, agnostic=False)
        t2 = time_synchronized()

        # Apply Classifier
        if classify:
            pred = apply_classifier(pred, modelc, img, im0s)

        # Process detections
        for i, det in enumerate(pred):  # detections per image
            p, s, im0, frame = path, '', im0s, getattr(dataset, 'frame', 0)

            p = Path(p)  # to Path
            save_path = str(Path(save_dir_imgs) / p.name)  # img.jpg
            txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # img.txt
            s += '%gx%g ' % img.shape[2:]  # print string
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    if save_txt:  # Write to file
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                        line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format
                        with open(txt_path + '.txt', 'a') as f:
                            f.write(('%g ' * len(line)).rstrip() % line + '\n')

                    if save_img:  # Add bbox to image
                        label = f'{names[int(cls)]} {conf:.2f}'
                        plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=3)

            # Save results (image with detections)
            if save_img:
                if dataset.mode == 'image':
                    cv2.imwrite(save_path, im0)
                else:  # 'video'
                    if vid_path != save_path:  # new video
                        vid_path = save_path
                        if isinstance(vid_writer, cv2.VideoWriter):
                            vid_writer.release()  # release previous video writer

                        fourcc = 'mp4v'  # output video codec
                        fps = vid_cap.get(cv2.CAP_PROP_FPS)
                        w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*fourcc), fps, (w, h))
                    vid_writer.write(im0)

    if save_txt or save_img:
        s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default='../source_tailgating/yolov5s.pt', help='model.pt path(s)')
    parser.add_argument('--source', type=str, default='/media/sagar/New Volume/everything/job/Seneca/data/making_vid/tailgatin_data/too_close/images', help='source')  
    parser.add_argument('--img-size', type=int, default=1280, help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='IOU threshold for NMS')
    parser.add_argument('--device', default='0', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--save-txt', action='store_true', default = "text.txt",help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
    parser.add_argument('--output_folder', default='/media/sagar/New Volume/everything/job/Seneca/data/making_vid/tailgatin_data/too_close/labels/', help='where you wish to save the labels')
    opt = parser.parse_args()
    print(opt)

    with torch.no_grad():
        detect(opt.weights, opt.source, opt.img_size, opt.conf_thres, opt.iou_thres, opt.device, opt.save_txt, opt.save_conf, opt.classes, opt.output_folder)