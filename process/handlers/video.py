import cv2
import os
import math

from setup.folders import initialize_folder

from preprocess.time.axis_xml import add_frame_offset_to_time
from process.tracker.centroid import Tracker
from process.color.blob_detection import get_top_color
from postprocess.image.editor import write_bounding_boxes_to_image, write_image
from postprocess.database import Database

ALLOWED_BODIES = ["sedan", "suv", "truck", "van"]

def parse_video_for_local(detect_model, classify_model, cap, video_builder, detect_folder, crop_folder, classify_buffer=[], caption_buffer=[], count=0, start_time="1999-12-31 00:00:00"):
    annotated_folder = os.path.join(detect_folder, "annotated")
    original_folder = os.path.join(detect_folder, "original")
    
    initialize_folder(annotated_folder)
    initialize_folder(original_folder)

    success, image = cap.read()
    
    frame = 1
    curr_time = start_time

    tracker = Tracker(max_x=image.shape[1], max_y=image.shape[0])

    while success:
        results = detect_model.run(image=image)
        annotated = image.copy()

        for dims in results:
            x_min, y_min, x_max, y_max = math.floor(dims[0]), math.floor(dims[1]), math.ceil(dims[2]), math.ceil(dims[3])
            
            det = image[y_min:y_max, x_min:x_max]
            
            tracker.determine(x_min, y_min, x_max, y_max, det, frame)

            annotated = write_bounding_boxes_to_image(x_min, y_min, x_max, y_max, annotated, (20, 20, 255), 3)
        
        if len(caption_buffer) > 0:
            if caption_buffer[0]["start"] + 40 == frame:
                caption_buffer.pop(0)
        
        classify_buffer.extend(tracker.decrement(time=str(frame)))

        if len(classify_buffer) > 0:
            write_image(os.path.join(detect_folder, "annotated"), annotated, str(frame))
            write_image(os.path.join(detect_folder, "original"), image, str(frame))
        
        video_builder.write(og_image=annotated, texts=[caption["text"] for caption in caption_buffer], count=count, time=curr_time)

        # Only run classification model if there are no objects being tracked
        if tracker.is_empty() and len(classify_buffer) > 0:
            obj = classify_buffer.pop(0)
 
            obj['type'] = classify_model.run(obj['image'])
            if obj['type'].lower() in ALLOWED_BODIES:
                obj['color'] = get_top_color(obj['image'])
                
                count += 1 if obj['enter'] else -1
                
                caption_buffer.append({
                    "text": f"Car detected: {obj['color']} {obj['type']} {'entered' if obj['enter'] else 'exited'}",
                    "start": frame
                })
                
                write_image(crop_folder, obj['image'], f"{obj['appeared']}_{str(frame)}_{obj['color']}_{obj['type']}")

        success, image = cap.read()
        frame += 1
        curr_time = add_frame_offset_to_time(start_time, frame)
        
    return {
        "classify": classify_buffer,
        "caption": caption_buffer,
        "count": count
    }

def parse_video_for_db(detect_model, classify_model, cap, db, classify_buffer=[], count=0, start_time="1999-12-31 00:00:00"):
    success, image = cap.read()
    
    frame = 1
    curr_time = start_time

    tracker = Tracker(max_x=image.shape[1], max_y=image.shape[0])

    while success:
        results = detect_model.run(image=image)
        annotated = image.copy()

        for dims in results:
            x_min, y_min, x_max, y_max = math.floor(dims[0]), math.floor(dims[1]), math.ceil(dims[2]), math.ceil(dims[3])
            
            det = image[y_min:y_max, x_min:x_max]
            
            tracker.determine(x_min, y_min, x_max, y_max, det, frame)

            annotated = write_bounding_boxes_to_image(x_min, y_min, x_max, y_max, annotated, (20, 20, 255), 3)
        
        classify_buffer.extend(tracker.decrement(time=str(frame)))

        # Only run classification model if there are no objects being tracked
        if tracker.is_empty() and len(classify_buffer) > 0:
            obj = classify_buffer.pop(0)
 
            obj['type'] = classify_model.run(obj['image'])

            if obj['type'].lower() in ALLOWED_BODIES:
                obj['color'] = get_top_color(obj['image'])
                
                count += 1 if obj['enter'] else -1
                
                db.insert(count, curr_time, obj['color'], obj['type'], 'in' if obj['enter'] else 'out')

        success, image = cap.read()
        frame += 1
        curr_time = add_frame_offset_to_time(start_time, frame)
        
    return {
        "classify": classify_buffer,
        "count": count
    }