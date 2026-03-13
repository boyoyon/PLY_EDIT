import numpy as np
import open3d as o3d
import os, sys

argv = sys.argv
argc = len(argv)

print('%s twists the mesh' % argv[0])
print('[usage] python %s <mesh> <angle>' % argv[0])

if argc < 3:
    quit()

mesh = o3d.io.read_triangle_mesh(argv[1])
center = mesh.get_center()
mesh.translate(-center)

vertices = np.array(mesh.vertices)

_min = np.min(vertices[:,1])
_max = np.max(vertices[:,1])
_width = _max - _min

angle = np.deg2rad(float(argv[2]))

for p in vertices:

    x = p[0]
    y = p[1]
    z = p[2]

    scale = (y - _min) / _width
    a = angle * scale

    xx = np.cos(a) * x - np.sin(a) * z
    zz = np.sin(a) * x + np.cos(a) * z

    p[0] = xx
    p[2] = zz

mesh.vertices = o3d.utility.Vector3dVector(vertices)
mesh.translate(center)

base = os.path.basename(argv[1])
filename = os.path.splitext(base)[0]
dst_path = '%s_twisted.ply' % filename
o3d.io.write_triangle_mesh(dst_path, mesh)
print('save %s' % dst_path)
  
   



   
    

