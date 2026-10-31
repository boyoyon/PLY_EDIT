import numpy as np
import open3d as o3d
import os, sys

argv = sys.argv
argc = len(argv)

print('%s loads mesh ply and outputs pcd ply' % argv[0])
print('[usage] python %s <mesh ply>' % argv[0])

if argc < 2:
    quit()

mesh = o3d.io.read_triangle_mesh(argv[1])
vertices = np.asarray(mesh.vertices)
triangles = np.asarray(mesh.triangles)
colors = np.asarray(mesh.vertex_colors)

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(vertices)
pcd.colors = o3d.utility.Vector3dVector(colors)

base = os.path.basename(argv[1])
filename = os.path.splitext(base)[0]
dst_path = '%s_pcd.ply' % filename
o3d.io.write_point_cloud(dst_path, pcd)
print('save %s' % dst_path)

