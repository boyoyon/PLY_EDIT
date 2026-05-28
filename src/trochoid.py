import cv2, random, sys
import numpy as np

SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512
MARGIN = 25

scale = -1.0
bias = -1.0

TH = 0.0018

def warp(u):

    U = int(u * scale + bias)

    return U

def rotate2D(x, y, theta):

    theta -= np.pi / 2

    X = np.cos(theta) * x - np.sin(theta) * y
    Y = np.sin(theta) * x + np.cos(theta) * y

    return X, Y

def epitrochoid(x, y, rFIX, rMOV, thetaL):

    thetaS = thetaL * rFIX / rMOV

    x1, y1 = rotate2D(x, y, thetaS)
    x2 = x1 + rFIX + rMOV
    y2 = y1
    x3, y3 = rotate2D(x2, y2, thetaL)
    x4 = warp(x3)
    y4 = warp(y3)

    return x4, y4

def epitrochoidV(V, rFIX, rMOV, thetaL):

    _V = []

    for v in V:

        x = v[0]
        y = v[1]

        X, Y = epitrochoid(x, y, rFIX, rMOV, thetaL)

        _V.append((X, Y))

    return _V

def generate_f(r):

    F = []
    
    R = r * 0.35

    F.append(( 1.5 * R,  2 * R))
    F.append((-1.5 * R,  2 * R))
    F.append((-1.5 * R,  1 * R))
    F.append(( 0.5 * R,  1 * R))
    F.append(( 0.5 * R,  0.5 * R))
    F.append((-0.75 * R,  0.5 * R))
    F.append((-0.75 * R, -0.5 * R))
    F.append(( 0.5 * R, -0.5 * R))
    F.append(( 0.5 * R, -1.75 * R))
    F.append(( 1.5 * R, -1.75 * R))

    return F

def main():

    global scale, bias

    argv = sys.argv
    argc = len(argv)
    
    print('%s draws epitrochoid curve' % argv[0])
    print('[usage] python %s [<length> <ratio of moving wheel> <ratio of fixed wheel>]' % argv[0])
    print()
    
    length = 1
    ratioMovingWheel = 1
    ratioFixedWheel = 1

    if argc > 1:
        length = float(argv[1])

    if argc > 2:
        ratioMovingWheel = int(argv[2])
    
    if argc > 3:
        ratioFixedWheel = int(argv[3])
    
    WHITE = (255, 255, 255)
    
    rFIX = 3.0
    
    ratio = ratioMovingWheel / ratioFixedWheel
    
    rMOV = rFIX * ratio
   
    if length >= 1:
        scale = (SCREEN_HEIGHT - MARGIN * 2) / ((rFIX + rMOV + rMOV * length) * 2)
    else:
        scale = (SCREEN_HEIGHT - MARGIN * 2) / ((rFIX + rMOV + rMOV) * 2)

    bias = SCREEN_HEIGHT / 2
    
    screen = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH, 3), np.uint8)
    screen2 = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH, 3), np.uint8)
    
    Rfixed = int(rFIX * scale)
    Rmoving = int(rMOV * scale)
    
    XCfixed = warp(0)
    YCfixed = warp(0)
    
    x = 0
    y = rMOV * length
    
    COLOR = (255, 255, 0)
    
    nDiv = 10 + int(ratio * 100)
    
    key = -1
    
    delta = np.pi * 2 * ratio / nDiv
    theta = 0 
      
    terminate = False
    wait_time = 10
    flag_pause = False
    flag_init_stop = True

    f = generate_f(rMOV)
    
    PrevX = -1
    PrevY = -1

    fTerminate = False
    points = []

    print('Hit p-key to pause / restart')
    print('Hit s-key to save and terminate')
    print('Hit q-key or ESC-key to quit')

    start = None

    while key != 27 and key != ord('q') and key != ord('Q') and key != ord('s') and key != ord('S'):
    
        for i in range(nDiv+1):
       
            cv2.circle(screen, (XCfixed, YCfixed), Rfixed, WHITE, 1)
            X, Y = epitrochoid(x, y, rFIX, rMOV, theta)
            if not fTerminate:
                points.append((X/(SCREEN_WIDTH+MARGIN*2),Y/(SCREEN_HEIGHT+MARGIN*2),0.0)) 

                if len(points) == 1:
                    start = np.array(points[0])
                else:
                    end = np.array(points[-1])
                    l = np.linalg.norm(end-start)
                    if l < TH:
                        fTerminate = True
                        print('stop storing points') 
    
            F = epitrochoidV(f, rFIX, rMOV, theta)
   
            cv2.circle(screen, (X, Y), 10, COLOR, -1)
    
            if PrevX >= 0 and PrevY >= 0:
                cv2.line(screen2, (X, Y), (PrevX, PrevY), COLOR, 2)
                
            PrevX = X
            PrevY = Y

            for i in range(len(F)-1):
                j = i + 1
                cv2.line(screen, F[i], F[j], WHITE, 1)
    
            cv2.line(screen, F[0], F[-1], WHITE, 1)
    
            XC, YC = epitrochoid(0, 0, rFIX, rMOV, theta)
            cv2.circle(screen, (XC, YC), Rmoving, WHITE, 1)
          
            if length > 1:
                cv2.line(screen, (XC, YC), (X, Y), WHITE, 2)
            
            # 背景: 黒
            cv2.imshow('screen', screen + screen2)
            # 背景: 白
            #cv2.imshow('screen', 255 - screen - screen2)
            
            if flag_pause or flag_init_stop:
                key = cv2.waitKey(0)
                flag_init_stop = False
            else:
                key = cv2.waitKey(wait_time)
       
            if key == 27 or key == ord('q') or key == ord('Q') or key == ord('s') or key == ('S'):
                terminate = True
                break
    
            elif key == ord('p') or key == ord('P'):
    
                if flag_pause:
                    flag_pause = False
                else:
                    flag_pause = True
    
            if cv2.getWindowProperty('screen', cv2.WND_PROP_VISIBLE) <= 0:
                terminate = True
                break
            
            screen = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH, 3), np.uint8)
    
            theta += delta
   
    if key == ord('s') or key == ord('S'):

        np.save('trochoid.npy', points)
        print('save trochoid.npy')

        cv2.imwrite('trochoid.png', screen2)
        print('save trochoid.png')

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

