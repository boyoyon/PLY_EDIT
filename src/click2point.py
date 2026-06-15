import numpy as np
import cv2, os, sys

H = -1
W = -1

mouse_x = -1
mouse_y = -1
Lstate = -1
Rstate = -1

points = []
fUpdate = True

def mouse_callback(event, x, y, flags, param):

    global mouse_x, mouse_y, Lstate, Rstate, fUpdate
    
    mouse_x = x
    mouse_y = y

    if event == cv2.EVENT_LBUTTONDOWN:
        Lstate = 1
    
    if event == cv2.EVENT_LBUTTONUP:
        points.append((mouse_x / W, mouse_y / H, 0.0))
        fUpdate = True
        Lstate = 0

    if event == cv2.EVENT_RBUTTONDOWN:
        Rstate = 1
        Lstate = 0
    
    if event == cv2.EVENT_RBUTTONUP:
        points.pop()
        fUpdate = True
        Rstate = 0

def main():

    global H, W, fUpdate, points

    argv = sys.argv
    argc = len(argv)

    print('%s creates .npy from image by clicking points' % argv[0])
    print('[usage] python %s <image>' % argv[0])

    if argc < 2:
        quit()
    
    src = cv2.imread(argv[1]) 
    H, W = src.shape[:2]

    src //= 2 # darken

    screen = src.copy()
    cv2.imshow('screen', screen)
    cv2.setMouseCallback('screen', mouse_callback)

    key = -1

    print('Press Left button to add point')
    print('Press Right button to remove the last point')
    print('Hit s-key to save and terminate')
    print('Hit any other any key to quit')

    font = cv2.FONT_HERSHEY_PLAIN
    font_size = 1
    font_color = (0, 255, 0)

    R = 5

    while key == -1:

        if fUpdate:

            screen = src.copy()

            for i, p in enumerate(points):

                x = int(p[0] * W)
                y = int(p[1] * H)

                cv2.circle(screen, (x, y), R, (0, 255, 0), -1)
                cv2.putText(screen, '%d' % i, (x+5, y+5), font, font_size, font_color, 2)

            cv2.imshow('screen', screen)

            fUpdate = False

        key = cv2.waitKey(100)
    
    cv2.destroyAllWindows()

    if key == ord('s') or key == ord('S'):

        dst_path = 'click2point.png'
        cv2.imwrite(dst_path, screen)
        print('save %s' % dst_path)

        if len(points) > 0:

            dst_path = 'click2point.npy'

            points = np.array(points)
            points[:,0] -= 0.5
            points[:,1] = (1 - points[:,1]) - 0.5
            np.save(dst_path, points)
            print('save %s' % dst_path)

if __name__ == '__main__':
    main()
