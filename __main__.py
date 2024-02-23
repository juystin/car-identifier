import os
import argparse

from model.detect import DetectEngine
from model.classify import ClassifyEngine
from preprocess.setup import initialize_arguments, initialize_folder, reset_folder, get_source_type
from preprocess.source_types import SourceType

from processors.video import process_video
from processors.image import process_image

parser = argparse.ArgumentParser()
args = initialize_arguments(parser)

crops_folder = args.crops
detects_folder = args.detects

initialize_folder(crops_folder)
initialize_folder(detects_folder)

src_type = get_source_type(args.src)

detection_model = DetectEngine(src=args.detect, imgsz=416, conf=0.2)
color_model = ClassifyEngine(src=args.classify, imgsz=640)

if (src_type == SourceType.VID):
    det_video_folder = os.path.join(detects_folder, "video")
    crops_video_folder = os.path.join(crops_folder, "video")
    
    initialize_folder(det_video_folder)
    initialize_folder(crops_video_folder)
    
    det_individual_folder = os.path.join(det_video_folder, os.path.splitext(os.path.basename(args.src))[-2])
    crops_individual_folder = os.path.join(crops_video_folder, os.path.splitext(os.path.basename(args.src))[-2])
    
    reset_folder(det_individual_folder)
    reset_folder(crops_individual_folder)

    process_video(args.src, detection_model, color_model, det_individual_folder, crops_individual_folder)

elif (src_type == SourceType.IMG):
    det_image_folder = os.path.join(detects_folder, "image")
    crops_image_folder = os.path.join(crops_folder, "image")

    initialize_folder(det_image_folder)
    initialize_folder(crops_image_folder)
    
    det_individual_folder = os.path.join(det_image_folder, os.path.splitext(os.path.basename(args.src))[-2])
    crops_individual_folder = os.path.join(crops_image_folder, os.path.splitext(os.path.basename(args.src))[-2])
    
    reset_folder(det_individual_folder)
    reset_folder(crops_individual_folder)

    process_image(args.src, detection_model, color_model, det_individual_folder, crops_individual_folder)

elif (src_type == SourceType.DIR):
    for file in os.listdir(args.src):
        if get_source_type(os.path.join(args.src, file)) == SourceType.IMG:
            det_image_folder = os.path.join(detects_folder, "image")
            crops_image_folder = os.path.join(crops_folder, "image")

            initialize_folder(det_image_folder)
            initialize_folder(crops_image_folder)
            
            det_individual_folder = os.path.join(det_image_folder, os.path.splitext(file)[0])
            crops_individual_folder = os.path.join(crops_image_folder, os.path.splitext(file)[0])
            
            reset_folder(det_individual_folder)
            reset_folder(crops_individual_folder)

            process_image(os.path.join(args.src, file), detection_model, color_model, det_individual_folder, crops_individual_folder)
        elif get_source_type(os.path.join(args.src, file)) == SourceType.VID:
            det_video_folder = os.path.join(detects_folder, "video")
            crops_video_folder = os.path.join(crops_folder, "video")
            
            initialize_folder(det_video_folder)
            initialize_folder(crops_video_folder)
            
            det_individual_folder = os.path.join(det_video_folder, os.path.splitext(file)[0])
            crops_individual_folder = os.path.join(crops_video_folder, os.path.splitext(file)[0])
            
            reset_folder(det_individual_folder)
            reset_folder(crops_individual_folder)
            
            print(det_individual_folder)
            print(crops_individual_folder)

            process_video(os.path.join(args.src, file), detection_model, color_model, det_individual_folder, crops_individual_folder)
        else:
            print(f"File {file} not supported")