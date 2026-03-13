import numpy as np
import cv2

mouse_x = -1
mouse_y = -1
Lstate = -1
Rstate = -1

SCREEN_SIZE = 768
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def mouse_callback(event, x, y, flags, param):

    global mouse_x, mouse_y, Lstate, Rstate
    
    mouse_x = x
    mouse_y = y

    if event == cv2.EVENT_LBUTTONDOWN:
        Lstate = 1
    
    if event == cv2.EVENT_LBUTTONUP:
        Lstate = 0

    if event == cv2.EVENT_RBUTTONDOWN:
        Rstate = 1
        Lstate = 0
    
    if event == cv2.EVENT_RBUTTONUP:
        Rstate = 0

def getDrawingPoints(width, height, mode):

    prev_mouse_x = -1
    prev_mouse_y = -1
    prev_Rstate = -1

    _points = []
 
    screen = np.zeros((height, width,3), np.uint8)
    cv2.imshow('hand drawing', screen)
    cv2.setMouseCallback('hand drawing', mouse_callback)

    key = -1

    print('Press Left button and drag to record points')
    print('Press Right button to clear recorded points')
    print('Hit any key to terminate drawing')

    while key == -1:


        if Lstate == 1 and (mouse_x != prev_mouse_x or mouse_y != prev_mouse_y):

            _points.append((mouse_x, mouse_y))
            idx = len(_points) - 1 

            if idx > 0:
                cv2.line(screen, _points[idx-1], _points[idx], WHITE, 1)
                cv2.imshow('hand drawing', screen)

            prev_mouse_x = mouse_x
            prev_mouse_y = mouse_y

        if Rstate != prev_Rstate:

            if Rstate == 1 and prev_Rstate == 0:

                cv2.rectangle(screen, (0, 0), (SCREEN_SIZE - 1, SCREEN_SIZE - 1), BLACK, -1)
                cv2.imshow('hand drawing', screen)

                _points.clear()

            prev_Rstate = Rstate

        key = cv2.waitKey(100)
    
    cv2.destroyAllWindows()

    points = None

    if len(_points) > 0:
        _points = np.array(_points).astype(np.float64)
        _points[:,0] /= width
        _points[:,1] /= -height # flip up/down

        points = np.zeros((_points.shape[0], 3), np.float64)
        points[:,:2] = _points

        if mode == 1:
            z = np.arange(_points.shape[0]) / 100
            points[:,2] = z

        points -= np.mean(points, axis = 0)

    return points
