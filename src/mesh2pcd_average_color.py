import numpy as np
import open3d as o3d

def get_areas(vertices, triangles):
 
    areas = []
    nr_triangles = triangles.shape[0] 

    for i in range(nr_triangles):
 
        idx0 = triangles[i][0]
        idx1 = triangles[i][1]
        idx2 = triangles[i][2]

        A = vertices[idx0]
        B = vertices[idx1]
        C = vertices[idx2]
    
        AB = B - A
        AC = C - A
        
        # 外積を計算
        cross_prod = np.cross(AB, AC)
        # 外積の長さの半分が面積
        area = 0.5 * np.linalg.norm(cross_prod)
   
        areas.append(area)
 
    return np.asarray(areas)

def get_pcl_points_and_colors(vertices, triangles, colors, points_per_triangle = 1.0):

    nr_triangles = triangles.shape[0]

    areas = get_areas(vertices, triangles)
    min_area = np.min(areas)
    N = (areas + 1e-06) / (min_area + 1e-06) * points_per_triangle 

    pcl_p = []
    pcl_c = []

    for i in range(nr_triangles):

        if nr_triangles // 10 > 0 and i % (nr_triangles // 10) == 0:
            print('processing %d/%d' % (i+1, nr_triangles))

        n = int(N[i])

        if n > 0:

            idx0 = triangles[i][0]
            idx1 = triangles[i][1]
            idx2 = triangles[i][2]

            P0 = vertices[idx0]
            P1 = vertices[idx1]
            P2 = vertices[idx2]

            if colors.shape[0] > 0:
                C0 = colors[idx0]
                C1 = colors[idx1]
                C2 = colors[idx2]

            for j in range(n):

                # ランダムな点の生成 (一様分布)
                r1 = np.random.rand()
                r2 = np.random.rand()
    
                u = 1.0 - np.sqrt(r1)
                v = r2 * np.sqrt(r1)
    
                # ランダムな座標 
                P = (1 - u - v) * P0 + u * P1 + v * P2
                pcl_p.append(P)

                if colors.shape[0] > 0:

                    C = (C0 + C1 + C2) / 3
                    pcl_c.append(C)

    return np.array(pcl_p), np.array(pcl_c)

import os, sys

points_per_triangle = 1.0

argv = sys.argv
argc = len(argv)

print('%s loads mesh ply and outputs pcd ply' % argv[0])
print('[usage] python %s <mesh ply> [<points per triangle(%.1f)>]' % (argv[0], points_per_triangle))

if argc < 2:
    quit()

if argc > 2:
    points_per_triangle = float(argv[2])

print('mesh ply:%s, scale:%.1f' % (argv[1], points_per_triangle))

mesh = o3d.io.read_triangle_mesh(argv[1])
vertices = np.asarray(mesh.vertices)
triangles = np.asarray(mesh.triangles)
colors = np.asarray(mesh.vertex_colors)

pcl_points, pcl_colors = get_pcl_points_and_colors(vertices, triangles, colors, points_per_triangle)

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(pcl_points)

if colors.shape[0] > 0:
    pcd.colors = o3d.utility.Vector3dVector(pcl_colors)

base = os.path.basename(argv[1])
filename = os.path.splitext(base)[0]
dst_path = '%s_pcd_average_color.ply' % filename
o3d.io.write_point_cloud(dst_path, pcd)
print('save %s' % dst_path)

