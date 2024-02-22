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