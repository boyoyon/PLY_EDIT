import numpy as np

def ifs(type = 'tree'):

    a = [0.0 , 0.85, 0.2 ,-0.15]
    b = [0.0 , 0.04,-0.26, 0.28] 
    c = [0.0 ,-0.04, 0.23, 0.26]
    d = [0.16, 0.85, 0.22, 0.24]
    e = [0,0 , 0.0 , 0.0 , 0.0 ]
    f = [0.0 , 1.6 , 1.6 , 0.44]

    if type == 'tree0':

        a = [0.0 , 0.1 , 0.42, 0.42]
        b = [0.0 , 0.0 ,-0.42, 0.42] 
        c = [0.0 , 0.0 , 0.42,-0.42]
        d = [0.5 , 0.1 , 0.42, 0.42]
        e = [0,0 , 0.0 , 0.0 , 0.0 ]
        f = [0.0 , 0.2 , 0.2 , 0.2 ]

    elif type == 'tree':

        a = [0.05, 0.05, 0.46, 0.47, 0.43, 0.42]
        b = [0.0 , 0.0 ,-0.32,-0.15, 0.28, 0.26] 
        c = [0.0 , 0.0 , 0.39, 0.17,-0.25,-0.35]
        d = [0.6 ,-0.5 , 0.38, 0.42, 0.45, 0.31]
        e = [0,0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 ]
        f = [0.0 , 1.0 , 0.6 , 1.1 , 1.0 , 0.7 ]


    N = len(a)
    M = 25 * N

    s = 0
    p = []
    ip = [] 

    for i in range(N):
        p.append(np.abs(a[i] * d[i] - b[i] * c[i]))
        s += p[-1]
        ip.append(i)

    for i in range(N-1):
        k = i

        for j in range(i+1, N):
            if p[j] < p[k]:
                k = j
        p[i], p[k] = p[k], p[i]
        ip[i], ip[k] = ip[k], ip[i]

    r = M
    table = np.zeros((r), np.int32)

    for i in range(N):
        k = int(r * p[i] / s + 0.5)
        s -= p[i]

        while True:
            r -= 1
            table[r] = ip[i]
            k -= 1
            if k <= 0:
                break

    x = 0.0
    z = 0.0
    points = []

    for i in range(30000):
        j = table[np.random.randint(M)]
        t = a[j] * x + b[j] * z + e[j]
        z = c[j] * x + d[j] * z + f[j]
        x = t
        if i > 10:
             points.append((x, 0.0, z))
         
    return points

import cv2, sys

def main():

    argv = sys.argv
    argc = len(argv)

    print('%s create points using Iterated Function System' % argv[0])
    print('[usage] python %s <-/tree0/tree>' % argv[0])

    type = 'fern'

    if argc > 1:
        type = argv[1]

    points = ifs(type)

    dst_path = 'ifs_%s.npy' % type
    np.save(dst_path, points)
    print('save %s' % dst_path)

    points = np.array(points)
    xmin = np.min(points[:,0])
    points[:,0] -= xmin
    xmax = np.max(points[:,0])

    ymin = np.min(points[:,2])
    points[:,2] -= ymin
    ymax = np.max(points[:,2])

    if ymax > xmax:
        points *= 500/ymax
        points[:,2] += 5
        points[:,0] += 5+(ymax-xmax)/2
    else:
        points *= 500/xmax
        points[:,0] += 5
        points[:,2] += 5+(xmax-ymax)/2

    screen = np.ones((512,512), np.uint8)
    screen *= 255

    for i in range(points.shape[0]):

        x = int(points[i][0])
        y = 511 - int(points[i][2])
        screen[y][x] = 0

    cv2.imshow('screen', screen)

    dst_path = dst_path.replace('.npy', '.png')
    cv2.imwrite(dst_path, screen)
    print('save %s' % dst_path)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
 
if __name__ == '__main__':
    main()   
