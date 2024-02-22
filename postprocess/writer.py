import cv2
import os

def write_for_video(path, obj):
    cv2.imwrite(os.path.join(path, f"{obj['appeared']}_{obj['removed']}_{obj['color']}_{'enter' if obj['enter'] else 'exit'}.jpg"), obj['image'])