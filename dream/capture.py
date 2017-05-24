import cv2


CORNER_WINDOW_NAME = 'Dream Calibration'
CORNER_NAMES = ['lower-left', 'lower-right', 'upper-left', 'upper-right']
CORNER_FORMAT = 'Please select the {} corner.'
CORNER_SUCCESS = 'Calibration completed.'

cap = cv2.VideoCapture(0)


def get_corners():
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

    cv2.destroyWindow('CORNER_WINDOW_NAME') 
    print(CORNER_SUCCESS)
    return corners


def save_image():
    pass
