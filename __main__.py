import os

from setup.folders import initialize_folder, delete_folder
from setup.arguments import parse_arguments
from setup.files import load_video_files

from process.detect.engine import DetectEngine
from process.classify.engine import ClassifyEngine
from process.handlers.video import parse_video_for_local, parse_video_for_db

from postprocess.video.builder import VideoBuilder
from postprocess.database import Database

import argparse

args = parse_arguments(argparse.ArgumentParser())

if args.out == 'local':
    detect_model = DetectEngine(args.detect, args.dsz, args.conf)
    class_model = ClassifyEngine(args.classify, args.csz)
    
    initialize_folder(args.crops)
    initialize_folder(args.detects)
    
    video_save_name = os.path.basename(os.path.dirname(args.src)) if os.path.isdir(args.src) else os.path.splitext(os.path.basename(args.src))[0]
    
    video_builder = VideoBuilder(save_folder=args.detects, save_name=video_save_name, width=1024, height=576)
    
    classify_buffer = []
    caption_buffer = []
    count = 0
    
    for video in load_video_files(args.src):
        print(f"Parsing {video['name']}...")
        individual_detects_folder = os.path.join(args.detects, video['name'])
        individual_crops_folder = os.path.join(args.crops, video['name'])
        
        delete_folder(individual_detects_folder)
        delete_folder(individual_crops_folder)
        
        initialize_folder(individual_detects_folder)
        initialize_folder(individual_crops_folder)
        
        # Any objects left in the buffers and the count at the end of the video
        residue = parse_video_for_local(detect_model, class_model, video['file'], video_builder, individual_detects_folder, individual_crops_folder, classify_buffer, caption_buffer, count, video['start'])
        classify_buffer, caption_buffer, count = residue['classify'], residue['caption'], residue['count']
        
    video_builder.close()
elif args.out == 'db':
    detect_model = DetectEngine(args.detect, args.dsz, args.conf)
    class_model = ClassifyEngine(args.classify, args.csz)

    db = Database()

    classify_buffer = []
    count = db.get_latest_count() or 0
    
    for video in load_video_files(args.src):
        print(f"Parsing {video['name']}...")
        
        # Any objects left in the buffers and the count at the end of the video
        residue = parse_video_for_db(detect_model, class_model, video['file'], db, classify_buffer, count, video['start'])
        classify_buffer, count = residue['classify'], residue['count']
        
    db.close()
    



