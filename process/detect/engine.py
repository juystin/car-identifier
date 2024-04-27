from ultralytics import YOLO
import os

class DetectEngine():
    def __init__(self, src, imgsz, conf):
        self.src = src
        self.model = YOLO(src, task="detect")
        self.imgsz = imgsz
        self.conf = conf

    def run(self, image):
        result = self.model(image, conf=self.conf, verbose=False, imgsz=self.imgsz)[0]
        
        return result.boxes.xyxy.cpu().numpy().tolist()