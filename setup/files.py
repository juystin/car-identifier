import cv2
import os

from preprocess.time.axis_xml import get_start_time
from datetime import datetime

SUPPORTED_VID_FORMAT = ['mp4', 'mkv', 'avi', 'mov', 'wmv', 'flv', '3gp', 'webm']

# Returns video files in an array
def load_video_files(path):
    file_format = os.path.splitext(os.path.basename(path))[1]
    
    video_list = []
    if os.path.exists(path) and os.path.isdir(path):
        for file in sorted(os.listdir(path)):
            file_format = os.path.splitext(os.path.basename(file))[1]
            if any(file_format == '.' + format for format in SUPPORTED_VID_FORMAT):
                xml_file = os.path.join(path, os.path.splitext(file)[0] + '.xml')
                if os.path.exists(xml_file):
                    start_time = get_start_time(xml_file)
                else:
                    start_time = "1999-12-31 00:00:00"
                video_list.append({
                    "name": os.path.splitext(os.path.basename(file))[0],
                    "file": cv2.VideoCapture(os.path.join(path, file)),
                    "start": start_time
                })
            else:
                print(f"{file} not supported.")
    elif os.path.exists(path) and any(file_format == '.' + format for format in SUPPORTED_VID_FORMAT):
        file_format = os.path.splitext(os.path.basename(path))[1]
        xml_file = os.path.join(os.path.splitext(path)[0] + '.xml')
        if os.path.exists(xml_file):
            start_time = get_start_time(xml_file)
        else:
            start_time = "1999-12-31 00:00:00"
        video_list.append({
            "name": os.path.splitext(os.path.basename(path))[0],
            "file": cv2.VideoCapture(path),
            "start": start_time
        })
    else:
        print(f"{path} not supported.")

    return video_list