import math
import cv2

from postprocess.centroid_tracker import Tracker
from postprocess.writer import write_for_video

def process_video(video_path, detection_model, color_model, results_folder):
    cap = cv2.VideoCapture(video_path)

    success, image = cap.read()
    frame = 1

    tracker = Tracker(max_x=image.shape[1], max_y=image.shape[0])

    classification_buffer = []

    while success:
        results = detection_model.run(image=image, name=str(frame))

        for dims in results:
            x_min, y_min, x_max, y_max = math.floor(dims[0]), math.floor(dims[1]), math.ceil(dims[2]), math.ceil(dims[3])
            
            det = image[y_min:y_max, x_min:x_max]
            
            tracker.determine(x_min, y_min, x_max, y_max, det, frame)
        
        classification_buffer.extend(tracker.decrement(time=str(frame)))
        
        # Only run classification model if there are no objects being tracked
        if tracker.is_empty() and len(classification_buffer) > 0:
            obj = classification_buffer.pop(0)
            obj['color'] = color_model.run(obj['image'])
            
            write_for_video(results_folder, obj)
            
        success, image = cap.read()
        frame += 1