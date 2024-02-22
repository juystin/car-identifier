# car-identifier

## Overview
car-identifier is a Python script designed to track the centroids of vehicles in a given video or image sequence. It utilizes neural networks to detect and classify vehicles, providing valuable insights for various applications such as traffic analysis, surveillance, and autonomous driving.

## Features
- Neural network models: The script uses neural network models trained with the YOLO architecture to detect and crop cars in a source video or image.
- Object tracking: Accurately tracks detected objects using a centroid tracking algorithm.
- Visualization: Provides frames of the tracked objects, allowing for easy interpretation of the results.
- Performance optimization: Utilizes .engine, a specialized model for NVIDIA-cards.

## Installation
Install requirements via ```pip install -r requirements.txt```

## Usage
```python car-identifier --detect [path to detection model] --classify [path to classification model] --src [path to source image or video] --results [path to results directory] --detect_frames [path to cropped detections directory]```