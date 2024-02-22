from postprocess.centroid_math import get_centroid, get_area, get_euclidean_distance, bounds_within_limits, centroid_in_top_half

import random

class Tracker():
    def __init__(self, max_x, max_y, alive_time=8, max_distance=200):
        self.alive_time = alive_time
        self.max_distance = max_distance
        self.max_x = max_x
        self.max_y = max_y
        
        self.tracked = []
    
    def get_tracked(self, centroid):
        objects_below_max_distance = [(obj, get_euclidean_distance(centroid, obj['centroid'])) for obj in self.tracked if get_euclidean_distance(centroid, obj['centroid']) < self.max_distance]
        if not objects_below_max_distance:
            return -1
        
        min_obj = min(objects_below_max_distance, key=lambda item: item[1])
        return min_obj['id']
    
    def create_id(self):
        return random.randint(0, 1000000)
    
    def add_to_tracked(self, centroid, area, image, time):
        self.tracked.append({
            "id": self.create_id(),
            "centroid": centroid,
            "area": area,
            "image": image,
            "alive_time": self.alive_time,
            "appeared": time,
            "enter": True if not centroid_in_top_half(centroid, self.max_y) else False
        })
        
    def update_tracked(self, obj_id, centroid, area, image):
        for obj in self.tracked:
            if obj['id'] == obj_id:
                obj['alive_time'] = self.alive_time
                obj['centroid'] = centroid
                if obj['area'] < area:
                    obj['area'] = area
                    obj['image'] = image
        
    def decrement(self, time):
        removed = []
        
        for obj in self.tracked:
            obj['alive_time'] -= 1
            if obj['alive_time'] <= 0:
                obj['removed'] = time
                removed.append(obj)
                self.tracked.remove(obj)
                
        return removed
                
    def determine(self, x_min, y_min, x_max, y_max, det, time):
        if bounds_within_limits(x_min, y_min, x_max, y_max, self.max_x, self.max_y):
            centroid = get_centroid(x_min, y_min, x_max, y_max)
            area = get_area(x_min, y_min, x_max, y_max)
            
            tracking_id = self.get_tracked(centroid)
            
            if tracking_id == -1:
                self.add_to_tracked(centroid, area, det, time)
            else:
                self.update_tracked(tracking_id, centroid, area, det)
            
    def is_empty(self):
        return len(self.tracked) == 0