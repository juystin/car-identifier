import os

DEFAULT_SRC = "test/sample.mp4"
DEFAULT_DETECTION_MODEL = "trained/detect/yadm.engine"
DEFAULT_DETECTION_SIZE = 640
DEFAULT_CONFIDENCE = 0.4
DEFAULT_CLASSIFICATION_MODEL = "trained/classify/type.engine"
DEFAULT_CLASSIFICATION_SIZE = 224

def parse_arguments(parser):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Get the base directory of the workspace

    parser.add_argument("--detect", help="Location of detection .engine model", nargs='?', const=os.path.join(base_dir, DEFAULT_DETECTION_MODEL), default=os.path.join(base_dir, DEFAULT_DETECTION_MODEL))
    parser.add_argument("--dsz", help="Image size of detection model", nargs='?', const=DEFAULT_DETECTION_SIZE, default=DEFAULT_DETECTION_SIZE)
    parser.add_argument("--conf", help="Minimum confidence of detections", nargs='?', const=DEFAULT_CONFIDENCE, default=DEFAULT_CONFIDENCE)
    parser.add_argument("--classify", help="Directory of classification .engine model", nargs='?', const=os.path.join(base_dir, DEFAULT_CLASSIFICATION_MODEL), default=os.path.join(base_dir, DEFAULT_CLASSIFICATION_MODEL))
    parser.add_argument("--csz", help="Image size of classification model", nargs='?', const=DEFAULT_CLASSIFICATION_SIZE, default=DEFAULT_CLASSIFICATION_SIZE)

    parser.add_argument("--crops", help="Directory to store crops", nargs='?', const=os.path.join(os.getcwd(), 'crops'), default=os.path.join(os.getcwd(), 'crops'))
    parser.add_argument("--detects", help="Directory to store detection results", nargs='?', const=os.path.join(os.getcwd(), 'detections'), default=os.path.join(os.getcwd(), 'detections'))
    
    parser.add_argument("--src", help="Location of file to parse", nargs='?', const=os.path.join(base_dir, DEFAULT_SRC), default=os.path.join(base_dir, DEFAULT_SRC))
    parser.add_argument("--out", help="Type to save output as: can be 'local' or 'db'. Defaults to 'local'. If using db, provide necessary .env file to authenticate. If using db, crops and detects flags are IGNORED", nargs='?', const='local', default='local')
    
    return parser.parse_args()
