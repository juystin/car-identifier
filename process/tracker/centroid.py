import random
import math

def get_centroid(x_min, y_min, x_max, y_max):
    return (x_min + x_max) / 2, (y_min + y_max) / 2

def get_area(x_min, y_min, x_max, y_max):
    return (x_max - x_min) * (y_max - y_min)

def get_euclidean_distance(centroid1, centroid2):
    return math.sqrt((centroid2[0] - centroid1[0]) ** 2 + (centroid2[1] - centroid1[1]) ** 2)

def bounds_within_limits(x_min, y_min, x_max, y_max, max_x, max_y, padding=20):
    return x_min >= padding and x_max <= max_x - padding and y_min >= padding and y_max <= max_y - padding

# Balance controls how much of the top the centroid must be in (0.5 being the middle of the frame, 0.25 being the top 25% of the frame, etc.)
def centroid_in_top_half(centroid, max_y, balance=0.35):
    return centroid[1] < max_y * balance
class Tracker():
    def __init__(self, max_x, max_y, alive_time=30, max_distance=300):
        self.alive_time = alive_time
        self.max_distance = max_distance
        self.max_x = max_x
        self.max_y = max_y
        
        self.tracked = []
    
    def get_tracked(self, centroid):
        objects_below_max_distance = [(obj, get_euclidean_distance(centroid, obj['centroid'])) for obj in self.tracked if get_euclidean_distance(centroid, obj['centroid']) < self.max_distance]
        if not objects_below_max_distance:
            return -1
        
        min_obj, min_distance = min(objects_below_max_distance, key=lambda item: item[1])
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