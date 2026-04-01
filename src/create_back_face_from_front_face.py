import numpy as np
import open3d as o3d
import os, sys

argv = sys.argv
argc = len(argv)

print('%s creates back face from the front face' % argv[0])
print('[usage] python %s <ply>' % argv[0])

if argc < 2:
    quit()

mesh = o3d.io.read_triangle_mesh(argv[1])
triangles = np.array(mesh.triangles)
mesh.triangles = o3d.utility.Vector3iVector(triangles[:,[0,2,1]])

colors = np.asarray(mesh.vertex_colors)
mesh.vertex_colors = o3d.utility.Vector3dVector(colors*0.4)

base = os.path.basename(argv[1])
filename = os.path.splitext(base)[0]
dst_path = '%s_back_face.ply' % filename
o3d.io.write_triangle_mesh(dst_path, mesh)
print('save %s' % dst_path)
