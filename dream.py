import os.path
import shelve
import tempfile

import boto3
import cv2
import numpy as np

S3_PUSH_KEY = 'dream_push.jpg'
S3_PULL_KEY = 'dream_pull.gzip'
NO_CALIBRATION_ERROR = 'Please calibrate before pushing.'
PUSH_WINDOW_NAME = 'Dream Push'
SHOW_IMAGE_TEXT = 'Showing image. Press any key to continue.'
ACCEPT_PUSH_QUESTION = 'Accept push?'

CALIBRATION_FILE = '.dream_calib'
CALIBRATION_PATH = os.path.join(os.path.expanduser('~'), CALIBRATION_FILE)

CORNER_WINDOW_NAME = 'Dream Calibration'
CORNER_NAMES = ['upper-left', 'upper-right', 'lower-left', 'lower-right']
CORNER_FORMAT = 'Please select the {} corner.'
CORNER_SUCCESS = 'Calibration completed.'

NO_PROCESS_TEXT = 'No process running.'

ec2 = boto3.resource('ec2')
s3 = boto3.resource('s3')


def run(args):
    cap = cv2.VideoCapture(0)
    bucket = s3.Bucket(args['bucket-name'])
    instance = ec2.Instance(args['instance-id'])
    if args['calibrate']:
        calibrate(cap)
    elif args['push']:
        width = int(args['image-width'])
        height = int(args['image-height'])
        push(instance, bucket, cap, width, height)
    elif args['pull']:
        pull(bucket)
    elif args['status']:
        status(instance, bucket)


def calibrate(cap):
    corners = get_corners(cap)
    with shelve.open(CALIBRATION_PATH) as db:
        db['corners'] = corners


def y_or_n(question):
    while True:
        text = '{} [Y/n] '.format(question)
        accept = input(text).lower()
        if accept == 'Y' or accept == '':
            return True
        elif accept.lower() == 'n':
            return False


def push(instance, bucket, cap, output_width, output_height):
    _, frame = cap.read()
    try:
        with shelve.open(CALIBRATION_PATH) as db:
            corners = db['corners']
    except FileNotFoundException:
        print(NO_CALIBRATION_ERROR)
        return
    output_size = (output_width, output_height)
    flat_frame = flatten(frame, corners, output_size)
    print(SHOW_IMAGE_TEXT)
    cv2.imshow(PUSH_WINDOW_NAME, flat_frame)
    cv2.waitKey(0)
    cv2.destroyWindow(PUSH_WINDOW_NAME)
    if not y_or_n(ACCEPT_PUSH_QUESTION):
        return
    path = save_frame(flat_frame)
    bucket.upload_file(path, S3_PUSH_KEY)
    instance.start()


def pull(bucket):
    bucket.download_file(S3_PULL_KEY, os.getcwd())
    

def status(instance, bucket):
    state = instance.state['Name']
    if state == 'running':
        temp = NamedTemporaryFile()
        bucket.download_file(S3_PULL_KEY, temp.name)
        with open(temp) as f:
            print(temp.read())
    else:
        print(NO_PROCESS_TEXT)


def get_corners(cap):
    _, frame = cap.read()
    cv2.namedWindow(CORNER_WINDOW_NAME)
    cv2.imshow(CORNER_WINDOW_NAME, frame)
    mouse_down = False
    mouse_x, mouse_y = 0, 0

    def corner_on_mouse(event, x, y, flags, params):
        nonlocal mouse_down, mouse_x, mouse_y
        if event == cv2.EVENT_LBUTTONDOWN:
            mouse_down = True
            mouse_x, mouse_y = x, y
            
    cv2.setMouseCallback(CORNER_WINDOW_NAME, corner_on_mouse)
    corners = []
    for corner_name in CORNER_NAMES:
        print(CORNER_FORMAT.format(corner_name))
        while not mouse_down:
            if cv2.waitKey(1) == 27:
                return
        corners.append((mouse_x, mouse_y))
        mouse_down = False
    cv2.destroyWindow(CORNER_WINDOW_NAME) 
    print(CORNER_SUCCESS)
    return corners


def flatten(frame, corners, output_size):
    new_corners = [(0, 0), (output_size[0], 0), (0, output_size[1]),
                   (output_size[0], output_size[1])]
    M = cv2.getPerspectiveTransform(np.float32(corners),
                                    np.float32(new_corners))
    return cv2.warpPerspective(frame, M, output_size)


def save_frame(frame):
    temp = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    cv2.imwrite(temp.name, frame)
    return temp.name
