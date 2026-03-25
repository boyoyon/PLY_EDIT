"""
y軸方向に伸びた円筒状の ply から 円筒表面から離れた点を含む三角形を削除する
だけのプログラム。

引数：(.plyファイル)　(半径)　(許容範囲)

"""

import numpy as np
from plyfile import PlyData
import os, sys

def save_ply(ply_path, X, Y, Z, triangles):

    with open(ply_path, mode='w') as f:

        line = 'ply\n'
        f.write(line)

        line = 'format ascii 1.0\n'
        f.write(line)

        line = 'element vertex %d\n' % X.shape[0]
        f.write(line)

        line = 'property float x\n'
        f.write(line)

        line = 'property float y\n'
        f.write(line)

        line = 'property float z\n'
        f.write(line)

        line = 'element face %d\n' % len(triangles)
        f.write(line)

        line = 'property list uchar int vertex_indices\n'
        f.write(line)

        line = 'end_header\n'
        f.write(line)

        for i in range(X.shape[0]):
            line = '%f %f %f \n' % (X[i], Y[i], Z[i])
            f.write(line)

        for i in range(len(triangles)):
            idx0 = triangles[i][0]
            idx1 = triangles[i][1]
            idx2 = triangles[i][2]
            
            line = '3 %d %d %d\n' % (idx0, idx1, idx2)
            f.write(line)

argv = sys.argv
argc = len(argv)

print('%s filetrs ply' % argv[0])
print('[usage] python %s <ply> <raidus> <margin>' % argv[0])

if argc < 3:
    quit()

r = float(argv[2])

margin = 0.1
if argc > 3:
    margin = float(argv[3])

TH = r * (1 - margin) ** 2

plyData = PlyData.read(argv[1])
X = plyData['vertex']['x']
Y = plyData['vertex']['y']
Z = plyData['vertex']['z']

faces = plyData['face'].data['vertex_indices']

triangles = []

for face in faces:

    if face.shape[0] != 3:
        continue

    idx = face[0]
    if X[idx] ** 2 + Z[idx] ** 2 < TH:
        continue

    idx = face[1]
    if X[idx] ** 2 + Z[idx] ** 2 < TH:
        continue

    idx = face[2]
    if X[idx] ** 2 + Z[idx] ** 2 < TH:
        continue

    triangles.append(face)

base = os.path.basename(argv[1])
filename = os.path.splitext(base)[0]
dst_path = '%s_filtered.ply' % filename

save_ply(dst_path, X, Y, Z, triangles)
print('save %s' % dst_path)
