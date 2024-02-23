import math
import cv2
import os

from preprocess.setup import initialize_folder
from postprocess.centroid_tracker import Tracker
from postprocess.writer import write_results_for_video, write_bounding_boxes_to_image, write_image

def process_video(video_path, detection_model, color_model, detection_folder, results_folder):
    cap = cv2.VideoCapture(video_path)

    success, image = cap.read()
    frame = 1

    tracker = Tracker(max_x=image.shape[1], max_y=image.shape[0])

    classification_buffer = []

    while success:
        results = detection_model.run(image=image)
        annotated = image.copy()

        for dims in results:
            x_min, y_min, x_max, y_max = math.floor(dims[0]), math.floor(dims[1]), math.ceil(dims[2]), math.ceil(dims[3])
            
            det = image[y_min:y_max, x_min:x_max]
            
            tracker.determine(x_min, y_min, x_max, y_max, det, frame)
            
            annotated_folder = os.path.join(detection_folder, "annotated")
            original_folder = os.path.join(detection_folder, "original")
            
            initialize_folder(annotated_folder)
            initialize_folder(original_folder)

            annotated = write_bounding_boxes_to_image(x_min, y_min, x_max, y_max, annotated, (15, 15, 255), 6)
        
        if (len(results) > 0):
            write_image(os.path.join(detection_folder, "annotated"), annotated, str(frame))
            write_image(os.path.join(detection_folder, "original"), image, str(frame))
        
        classification_buffer.extend(tracker.decrement(time=str(frame)))
        
        # Only run classification model if there are no objects being tracked
        if tracker.is_empty() and len(classification_buffer) > 0:
            obj = classification_buffer.pop(0)
            obj['color'] = color_model.run(obj['image'])
            
            write_results_for_video(results_folder, obj)
            
        success, image = cap.read()
        frame += 1