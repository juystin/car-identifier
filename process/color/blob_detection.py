import cv2
import matplotlib.pyplot as plt
import numpy as np

def get_top_color(image):
    # Convert the image to the HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for each color
    color_ranges = {
        'red': [([0, 70, 50], [10, 255, 255]), 
                ([160, 70, 50], [175, 255, 255])],
        'orange': [([11, 70, 50], [25, 255, 255])],
        'yellow': [([26, 70, 50], [35, 255, 255])],
        #'green': [([36, 70, 50], [70, 255, 255])],
        'blue': [([90, 70, 50], [140, 120, 140])],
        'black': [([0, 25, 40], [359, 75, 120])],
        'white': [([100, 0, 170], [125, 40, 255])],
        'silver': [([90, 0, 60], [125, 40, 180])]
    }

    # Create an empty mask
    mask = np.zeros(image.shape[:2], dtype=np.uint8)

    # Create a dictionary to store the areas of each color mask
    color_areas = {}

    # Iterate over each color range and create a mask for that color
    for color, ranges in color_ranges.items():
        for lower, upper in ranges:
            lower = np.array(lower, dtype=np.uint8)
            upper = np.array(upper, dtype=np.uint8)
            color_mask = cv2.inRange(hsv_image, lower, upper)
            mask = cv2.bitwise_or(mask, color_mask)

            # Calculate the area of the color mask and store it in the dictionary
            color_areas[color] = np.sum(color_mask == 255)

    return max(color_areas, key=color_areas.get)