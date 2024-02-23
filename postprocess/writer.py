import cv2
import os

def write_bounding_boxes_to_image(x_min, ymin, x_max, y_max, image, color, thickness):
    return cv2.rectangle(image.copy(), (x_min, ymin), (x_max, y_max), color, thickness)

def write_image(path, image, name):
    cv2.imwrite(os.path.join(path, f"{name}.jpg"), image)

def write_results_for_image(path, obj, image):
    cv2.imwrite(os.path.join(path, f"{obj['color']}.jpg"), image)

def write_results_for_video(path, obj):
    cv2.imwrite(os.path.join(path, f"{obj['appeared']}_{obj['removed']}_{obj['color']}_{'enter' if obj['enter'] else 'exit'}.jpg"), obj['image'])