import open3d as o3d
import numpy as np
import cv2, os, sys

param = 0.7

def create_fractal_terrain(H, W):

    screen = np.zeros((H,W), np.float32)

    for freq in [2, 4, 8, 16, 32, 64, 128, 256, 512]:
        img = (np.random.rand(freq, freq) - 0.5) / freq**param
        img = cv2.resize(img, (W, H))
        screen += img  

    screen -= np.min(screen)
    screen *= 255/np.max(screen)
    screen = np.clip(screen, 0, 255)
    screen = screen.astype(np.int32)

    return screen

argv = sys.argv
argc = len(argv)

print('%s creates texture by distorting image' % argv[0])
print('[usage] python %s <image>　[<param(default:0.7)>]' % argv[0])

if argc < 2:
    quit()

src = cv2.imread(argv[1])

if argc > 2:
    param = float(argv[2])

H, W = src.shape[:2]
scale = np.min((H, W)) // 50 + 1

screen = create_fractal_terrain(H, W)

dst = np.zeros((H-1, W-1, 3), np.uint8)

for y in range(H-1):

    if y % 50 == 0:
        print('processing %d/%d' % (y, (H-1)))

    y0 = y
    y1 = y + 1

    for x in range(W-1):

        x0 = x
        x1 = x + 1

        dy = (screen[y1][x] - screen[y0][x]) * scale
        dx = (screen[y][x1] - screen[y][x0]) * scale

        yy = np.min((H-1, np.max((0, y+dy))))
        xx = np.min((W-1, np.max((0, x+dx))))

        dst[y][x] = src[yy][xx]
       
base = os.path.basename(argv[1])
filename = os.path.splitext(base)[0]
dst_path = '%s_distorted.png' % filename
cv2.imwrite(dst_path, dst)
print('save %s' % dst_path)

