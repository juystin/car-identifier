import cv2
import os
import numpy as np

def get_base_image(width, height):
    return np.zeros((height, width, 3), dtype=np.uint8)

def overlay_image(large_image, small_image, x_offset, y_offset):
    y1, y2 = y_offset, y_offset + small_image.shape[0]
    x1, x2 = x_offset, x_offset + small_image.shape[1]

    if large_image[y1:y2, x1:x2].shape == small_image.shape:
        large_image[y1:y2, x1:x2] = small_image

    return large_image

def overlay_text(original_image, text, x_offset, y_offset, scale=0.5, thickness=1):
    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = scale
    font_thickness = thickness
    font_color = (255, 255, 255)
    line_type = cv2.LINE_AA

    image = original_image.copy()
    cv2.putText(image, text, (x_offset, y_offset), font, font_scale, font_color, font_thickness, line_type)
    return image

def rescale_image(image, factor):
    return cv2.resize(image, (0, 0), fx=factor, fy=factor)

class VideoBuilder():
    def __init__(self, save_folder, save_name, width=1600, height=900, fps=15):
        self.width = width
        self.height = height
        self.fps = fps
        self.path = os.path.join(save_folder, f"{save_name}.mp4")
        
        self.video = cv2.VideoWriter(self.path, cv2.VideoWriter_fourcc(*'MP4V'), fps, (width,height))
        
    def write(self, og_image, count, texts, time, factor=0.6):
        background = get_base_image(self.width, self.height)
        res_image = rescale_image(og_image, factor)
        
        frame_height, frame_width, _ = res_image.shape
        x_offset = int((self.width - frame_width) / 2)
        image = overlay_image(background, res_image, x_offset, 0)
        image = overlay_text(image, time, int(frame_width / 5), frame_height + 50, 0.6, 1)
        image = overlay_text(image, str(count), int(frame_width / 5), frame_height + 110, 1.5, 2)
        if texts:
            for i, text in enumerate(texts):
                image = overlay_text(image, text, int(frame_width / 3), frame_height + 110 + 15*i)
            
        self.video.write(image)
        
    def close(self):
        self.video.release()