import cv2, os, sys
import numpy as np

argv = sys.argv
argc = len(argv)

TOLERANCE = 0.001

print('%s extracts contour from the image' % argv[0])
print('[usage] python %s <image> [<tolerance>]' % argv[0]) 

if argc < 2:
    quit()

img = cv2.imread(argv[1], cv2.IMREAD_GRAYSCALE)

H = img.shape[0]
W = img.shape[1]

SIZE = np.max((H,W))

if argc > 2:
    TOLERANCE = float(argv[2])

contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

vertices = []

if contours:

    for cnt in contours:
        # 形状の周囲長を計算
        peri = cv2.arcLength(cnt, True)
        # 周囲長の 0.1% を許容誤差として近似 (この割合を調整してひずみ具合を制御)
        epsilon = TOLERANCE * peri
        approx = cv2.approxPolyDP(cnt, epsilon, True)

    # contours[0] は (N, 1, 2) の形なので (N, 2) に変換
    contour_points = approx.reshape(-1, 2).tolist()
    
    for point in contour_points:
        vertices.append((point[0]/SIZE, point[1]/SIZE, 0.0))

vertives = np.array(vertices)

base = os.path.basename(argv[1])
filename = os.path.splitext(base)[0]
dst_path = '%s_contour.npy' % filename

np.save(dst_path, vertices)
print('save %s' % dst_path)

