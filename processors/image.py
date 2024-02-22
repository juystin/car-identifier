import math
import os
import cv2

def process_image(image_path, detection_model, color_model, results_folder):
    image = cv2.imread(image_path)
    
    results = detection_model.run(image=image, name="car")
    
    for dims in results:
        x_min, y_min, x_max, y_max = math.floor(dims[0]), math.floor(dims[1]), math.ceil(dims[2]), math.ceil(dims[3])
        
        det = image[y_min:y_max, x_min:x_max]
        
        color = color_model.run(det)
        
        cv2.imwrite(os.path.join(results_folder, f"{color}.jpg"), det)