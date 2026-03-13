import copy, cv2, os, sys
import numpy as np
import mapbox_earcut as earcut
import open3d as o3d

argv = sys.argv
argc = len(argv)

TOLERANCE = 0.001

print('%s extracts contour from the image' % argv[0])
print('[usage] python %s <image> [<tolerance>]' % argv[0]) 

if argc < 2:
    quit()

img = cv2.imread(argv[1])
screen = img.copy()

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
H = img.shape[0]
W = img.shape[1]

SIZE = np.max((H,W))

if argc > 2:
    TOLERANCE = float(argv[2])

contours, hierarchy = cv2.findContours(imgGray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

vertices = []

if contours:

    for cnt in contours:
        # 形状の周囲長を計算
        peri = cv2.arcLength(cnt, True)
        # 周囲長の 0.1% を許容誤差として近似 (この割合を調整してひずみ具合を制御)
        epsilon = TOLERANCE * peri
        approx = cv2.approxPolyDP(cnt, epsilon, True)

    # contours[0] は (N, 1, 2) の形なので (N, 2) に変換
    contour_points = approx.reshape(-1, 2)

    rings = np.array([len(contour_points)])
    result = earcut.triangulate_float32(contour_points, rings)

    triangles = result.reshape(-1,3)

    for triangle in triangles:

        idx0 = triangle[0]
        idx1 = triangle[1]
        idx2 = triangle[2]

        p0 = contour_points[idx0]
        p1 = contour_points[idx1]
        p2 = contour_points[idx2]
        cv2.line(screen, p0, p1, (255, 255, 0),1)
        cv2.line(screen, p1, p2, (255, 255, 0),1)
        cv2.line(screen, p2, p0, (255, 255, 0),1)

    cv2.imshow('screen', screen)
    base = os.path.basename(argv[1])
    filename = os.path.splitext(base)[0]

    dst_path = '%s_triangle.png' % filename
    cv2.imwrite(dst_path, screen)
    print('save %s' % dst_path)

    print('Hit ESC key to abort')
    print('Hit any other key to save and terminate')
    key = cv2.waitKey(0)
    cv2.destroyAllWindows()

    if key != 27: # not ESC key

        nr_points = contour_points.shape[0]
        vertices = np.zeros((nr_points,3),np.float64)

        for i, point in enumerate(contour_points):
            vertices[i] = (point[0]/W, point[1]/H, 0)

        dst_path = '%s_contour.npy' % filename
        np.save(dst_path, vertices)
        print('save %s' % dst_path)
   
        front_color = np.array([0.5, 0.5, 1.0])   # dark blue
         
        meshFront = o3d.geometry.TriangleMesh()
        meshFront.vertices = o3d.utility.Vector3dVector(vertices)
        meshFront.triangles = o3d.utility.Vector3iVector(triangles)
        
        meshFront.paint_uniform_color(front_color)

        dst_path = '%s_A.ply' % filename
        o3d.io.write_triangle_mesh(dst_path, meshFront)
        print('save %s' % dst_path)

        back_color = np.array([0.8, 0.8, 1.0])   # light blue
         
        meshBack = o3d.geometry.TriangleMesh()
        meshBack.vertices = o3d.utility.Vector3dVector(vertices)
        
        trianglesBack = copy.deepcopy(triangles)
        trianglesBack = trianglesBack[:,[0,2,1]]
        meshBack.triangles = o3d.utility.Vector3iVector(trianglesBack)
        
        meshBack.paint_uniform_color(back_color)

        dst_path = '%s_AA.ply' % filename
        o3d.io.write_triangle_mesh(dst_path, meshBack)
        print('save %s' % dst_path)

