import os
import tempfile

import cv2
import numpy as np


CORNER_WINDOW_NAME = 'Dream Calibration'
CORNER_NAMES = ['upper-left', 'upper-right', 'lower-left', 'lower-right']
CORNER_FORMAT = 'Please select the {} corner.'
CORNER_SUCCESS = 'Calibration completed.'

cap = cv2.VideoCapture(0)


def get_corners():
    frame = grab_frame()
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

    cv2.destroyWindow('CORNER_WINDOW_NAME') 
    print(CORNER_SUCCESS)
    return corners


def grab_frame():
    return cap.read()[1]


def show_frame(name, frame):
    cv2.imshow(name, frame)
    cv2.waitKey(0)
    cv2.destroyWindow(name)


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
