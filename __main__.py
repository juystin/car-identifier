import os
import argparse

from model.detect import DetectEngine
from model.classify import ClassifyEngine
from preprocess.setup import initialize_folder, initialize_arguments, get_source_type
from preprocess.source_types import SourceType

from processors.video import process_video
from processors.image import process_image

parser = argparse.ArgumentParser()
args = initialize_arguments(parser)

results_folder = initialize_folder(args.results)
detects_folder = initialize_folder(args.detect_results)

src_type = get_source_type(args.src)

detection_model = DetectEngine(detects_folder=detects_folder, src=args.detect, imgsz=416, conf=0.6)
color_model = ClassifyEngine(src=args.classify, imgsz=640)

if (src_type == SourceType.VID):
    process_video(args.src, detection_model, color_model, results_folder)
        
elif (src_type == SourceType.IMG):
    process_image(args.src, detection_model, color_model, results_folder)

elif (src_type == SourceType.DIR):
    for file in os.listdir(args.src):
        detection_model.update_folder(initialize_folder(os.path.join(detects_folder, os.path.splitext(file)[0])))

        if get_source_type(os.path.join(args.src, file)) == SourceType.IMG:
            process_image(os.path.join(args.src, file), detection_model, color_model, results_folder)
        elif get_source_type(os.path.join(args.src, file)) == SourceType.VID:
            process_video(os.path.join(args.src, file), detection_model, color_model, results_folder)
        else:
            print(f"File {file} not supported")