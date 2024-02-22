# car-identifier

## Overview
car-identifier is a Python script designed to track the centroids of vehicles in a given video or image sequence. It utilizes neural networks to detect and classify vehicles, providing imagery and categorization for various applications such as traffic analysis and dataset compilation.

## Features
- NEURAL NETWORK MODELS: The script uses neural network models trained with the YOLO architecture to detect and crop cars in a source video or image.
- OBJECT TRACKING: Accurately tracks detected objects using a centroid tracking algorithm.
- VISUALIZATION: Provides frames of the tracked objects, allowing for easy interpretation of the results.
- OPTIMIZED PERFORMANCE: Utilizes .engine, a specialized model for NVIDIA-cards.

## Installation
```git clone https://github.com/juystin/car-identifier.git```
```pip install -r requirements.txt```

## Notes
.engine files are not provided. Public datasets are available for training via RoboFlow.

## Usage
```python car-identifier --detect [path to detection model] --classify [path to classification model] --src [path to source image or video] --results [path to results directory] --detect_frames [path to cropped detections directory]```
