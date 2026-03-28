import numpy as np
import open3d as o3d
from plyfile import PlyData, PlyElement
import os, sys

def is_inside_regular_polygon(x, y, nr_edges = 5, radius = 1):

    th = radius * np.cos(np.pi / nr_edges)
 
    for k in range(nr_edges):
        theta = 2 * np.pi * k / nr_edges
        # 各辺の内側（原点側）に点があるかチェック
        if x * np.cos(theta) + y * np.sin(theta) > th:
            return False  # 一つでも外側にあればアウト
    return True  # すべての条件を満たせば内部

argv = sys.argv
argc = len(argv)

print('%s prunes triangls overflows regular polygon' % argv[0])
print('[usage] python %s <.ply> <nr_edges> <radius>' % argv[0])

if argc < 4:
    quit()

plyData = PlyData.read(argv[1])
nr_edges = int(argv[2])
r = float(argv[3])

vertex_element = plyData['vertex']

X = plyData['vertex']['x']
Y = plyData['vertex']['y']
Z = plyData['vertex']['z']

faces = plyData['face'].data['vertex_indices']

triangles = []

for face in faces:

    if face.shape[0] != 3:
        continue

    idx = face[0]
    if not is_inside_regular_polygon(X[idx], Z[idx], nr_edges, r):
        continue
    
    idx = face[1]
    if not is_inside_regular_polygon(X[idx], Z[idx], nr_edges, r):
        continue
    
    idx = face[2]
    if not is_inside_regular_polygon(X[idx], Z[idx], nr_edges, r):
        continue
    
    triangles.append(face)

triangles = np.array(triangles)

face_dtype = [('vertex_indices', 'i4', (3,))] 
structured_faces = np.empty(triangles.shape[0], dtype=face_dtype)
structured_faces['vertex_indices'] = triangles
pruned_face_element = PlyElement.describe(structured_faces, 'face')

pruned_plyData = PlyData([vertex_element, pruned_face_element], text=False)

base = os.path.basename(argv[1])
filename = os.path.splitext(base)[0]
dst_path = '%s_pruned.ply' % filename

pruned_plyData.write(dst_path)
print('save %s' % dst_path)
