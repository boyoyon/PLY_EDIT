from plyfile import PlyData
import numpy as np
import os, sys

argv = sys.argv
argc = len(argv)

print('%s converts ply to skeleton data(.npy)' % argv[0])
print('[usage] python %s <ply>' % argv[0])

if argc < 2:
    quit()

plydata = PlyData.read(argv[1])
X = plydata['vertex']['x']
Y = plydata['vertex']['y']
Z = plydata['vertex']['z']

faces = plydata['face'].data['vertex_indices']

triangles = []

for face in faces:

    if face.shape[0] != 3:
        continue

    p = []    
    idx = face[0]
    p.append((X[idx], Y[idx], Z[idx]))

    idx = face[1]
    p.append((X[idx], Y[idx], Z[idx]))

    idx = face[2]
    p.append((X[idx], Y[idx], Z[idx]))

    triangles.append(p)

triangles = np.array(triangles)

base = os.path.basename(argv[1])
filename = os.path.splitext(base)[0]
dst_path = '%s_skeleton.npy' % filename

np.save(dst_path, triangles)
print('save %s' % dst_path)
