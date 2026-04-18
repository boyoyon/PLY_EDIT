import open3d as o3d
import numpy as np
import cv2, sys

size = 100
param = 0.975

def create_fractal_terrain(size=50):
    # 1. グリッドの生成
    xx = np.linspace(-1, 1, size)
    zz = np.linspace(-1, 1, size)
    x, z = np.meshgrid(xx, zz)
    
    # 2. 高さ(z)にフラクタル的なノイズを付与（簡易版）
    y = np.zeros((size, size))
    #for freq in [1, 2, 4, 8]:
    for freq in [2, 4, 8, 16, 32, 64, 128, 256, 512]:
        img = (np.random.rand(freq, freq) - 0.5) / freq**param
        img = cv2.resize(img, (size, size))
        y += img  

    # 3. 頂点と三角形のインデックス作成
    vertices = np.stack([x.ravel(), y.ravel(), z.ravel()], axis=1)
    triangles = []
    for i in range(size - 1):
        for j in range(size - 1):
            v = i * size + j
            triangles.append([v, v + size, v + 1])
            triangles.append([v + 1, v + size, v + size + 1])


    meshFront = o3d.geometry.TriangleMesh()
    meshFront.vertices = o3d.utility.Vector3dVector(vertices)
    meshFront.triangles = o3d.utility.Vector3iVector(np.array(triangles))
    meshFront.paint_uniform_color([0.2, 0.6, 0.2]) # 緑色
    meshFront.compute_vertex_normals()

    meshBack = o3d.geometry.TriangleMesh()
    meshBack.vertices = o3d.utility.Vector3dVector(vertices)
    meshBack.triangles = o3d.utility.Vector3iVector(np.array(triangles)[:,[0,2,1]])
    meshBack.paint_uniform_color([0.5, 0.6, 0.5]) # 緑色
    meshBack.compute_vertex_normals()
 
    return meshFront, meshBack

argv = sys.argv
argc = len(argv)

print('%s creates terrain' % argv[0])
print('[usage] python %s [<size (default:100)> <param (default:0.975)]' % argv[0])

if argc > 1:
    size = int(argv[1])

if argc > 2:
    param = float(argv[2])

terrainFront, terrainBack = create_fractal_terrain(size)
o3d.visualization.draw_geometries([terrainFront, terrainBack])

dst_path = 'terrainA.ply'
o3d.io.write_triangle_mesh(dst_path, terrainFront)
print('save %s' % dst_path)

dst_path = 'terrainAA.ply'
o3d.io.write_triangle_mesh(dst_path, terrainBack)
print('save %s' % dst_path)
