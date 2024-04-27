from ultralytics import YOLO

class ClassifyEngine():
    def __init__(self, src, imgsz):
        self.src = src
        self.model = YOLO(src, task="classify")
        self.imgsz = imgsz
    
    def run(self, image):
        result = self.model(image, verbose=False, imgsz=self.imgsz)[0]
            
        return result.names[result.probs.top5[0]]