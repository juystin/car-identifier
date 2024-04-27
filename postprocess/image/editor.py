import cv2
import os

def write_bounding_boxes_to_image(x_min, y_min, x_max, y_max, image, color, thickness):
    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, thickness)
    return image

def write_image(folder, image, name):
    cv2.imwrite(os.path.join(folder, f"{name}.jpg"), image)