import cv2
import numpy as np

def hsv2rgb(H, S, V):

    R = G = B = 0

    while H<0:
        H += 360

    while H>360:
        H -= 360

    H /= 60

    I = int(H)
    dF = (H - I)*255
    dM = V*(255-S)/255
    dN = V*(255-S*dF/255)/255
    dK = V*(255-S*(255-dF)/255)/255

    if I == 0:
         R = int(V)
         G = int(dK)
         B = int(dM)

    elif I == 1:
         R = int(dN)
         G = int(V)
         B = int(dM)

    elif I == 2:
         R = int(dM)
         G = int(V)
         B = int(dK)

    elif I == 3:
         R = int(dM)
         G = int(dN)
         B = int(V)

    elif I == 4:
         R = int(dK)
         G = int(dM)
         B = int(V)

    elif I == 5:
         R = int(V)
         G = int(dM)
         B = int(dN)

    return R, G, B


def main():

    HEIGHT = 100
    WIDTH = 360

    screen = np.empty((HEIGHT, WIDTH, 3), np.uint8)

    S = 200
    V = 200

    for H in range(WIDTH):

        R, G, B = hsv2rgb(H, S, V)

        screen = cv2.line(screen, (H, 0), (H, HEIGHT - 1), (B, G, R), 1)

    cv2.imshow('screen', screen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
