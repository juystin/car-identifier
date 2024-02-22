import os
import shutil

from preprocess.source_types import SourceType

SUPPORTED_IMG_FORMAT = ['jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff', 'webp']
SUPPORTED_VID_FORMAT = ['mp4', 'mkv', 'avi', 'mov', 'wmv', 'flv', '3gp', 'webm']

DEFAULT_SRC = "test/test_vid.mkv"
DEFAULT_DETECTION_MODEL = "trained/detect/detectv2.engine"
DEFAULT_CLASSIFICATION_DIR = "trained/classify/colorv4.engine"

def initialize_arguments(parser):
    parser.add_argument("--detect", help="Location of detection .engine model", nargs='?', const=os.path.join(os.path.dirname(os.path.abspath(__file__)), DEFAULT_DETECTION_MODEL), default=os.path.join(os.path.dirname(os.path.abspath(__file__)), DEFAULT_DETECTION_MODEL))
    parser.add_argument("--classify", help="Directory of classification .engine models", nargs='?', const=os.path.join(os.path.dirname(os.path.abspath(__file__)), DEFAULT_CLASSIFICATION_DIR), default=os.path.join(os.path.dirname(os.path.abspath(__file__)), DEFAULT_CLASSIFICATION_DIR))

    parser.add_argument("--results", help="Directory to store classification results", nargs='?', const=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results'), default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results'))
    parser.add_argument("--src", help="Location of image or video file to parse", nargs='?', const=os.path.join(os.path.dirname(os.path.abspath(__file__)), DEFAULT_SRC), default=os.path.join(os.path.dirname(os.path.abspath(__file__)), DEFAULT_SRC))
    parser.add_argument("--detect_results", help="Directory to store detection results", nargs='?', const=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'detections'), default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'detections'))
    
    return parser.parse_args()

def initialize_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.mkdir(folder_path)
    
    return folder_path

def get_source_type(source_path):
    if os.path.exists(source_path) and os.path.isdir(source_path):
        return SourceType.DIR
    elif os.path.exists(source_path) and any(source_path.endswith('.' + format) for format in SUPPORTED_IMG_FORMAT):
        return SourceType.IMG
    elif os.path.exists(source_path) and any(source_path.endswith('.' + format) for format in SUPPORTED_VID_FORMAT):
        return SourceType.VID