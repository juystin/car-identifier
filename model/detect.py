from ultralytics import YOLO
import os

class DetectEngine():
    def __init__(self, detects_folder, src, imgsz, conf):
        self.src = src
        self.model = YOLO(src, task="detect")
        self.imgsz = imgsz
        self.conf = conf
        self.detects_folder = detects_folder

    def update_folder(self, detects_folder):
        self.detects_folder = detects_folder

    def run(self, image, name):
        result = self.model(image, conf=self.conf, verbose=False, save=True, imgsz=self.imgsz, project=self.detects_folder, name=name)[0]
        
        return result.boxes.xyxy.cpu().numpy().tolist()