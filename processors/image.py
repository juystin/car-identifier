import math
import os
import cv2

from postprocess.writer import write_image, write_bounding_boxes_to_image, write_results_for_image

def process_image(image_path, detection_model, color_model, detection_folder, results_folder):
    image = cv2.imread(image_path)
    annotated = image.copy()
    
    results = detection_model.run(image=image)
    
    for dims in results:
        x_min, y_min, x_max, y_max = math.floor(dims[0]), math.floor(dims[1]), math.ceil(dims[2]), math.ceil(dims[3])
        
        det = image[y_min:y_max, x_min:x_max]
        
        color = color_model.run(det)
        
        obj = {
            "color": color
        }
        
        annotated = write_bounding_boxes_to_image(x_min, y_min, x_max, y_max, annotated, (15, 15, 255), 6)
        
    write_image(os.path.join(detection_folder, "annotated"), annotated, "results.jpg")
    write_image(os.path.join(detection_folder, "original"), image, "results.jpg")
    write_results_for_image(results_folder, obj, det)