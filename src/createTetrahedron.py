import cv2, os, sys
import numpy as np
from hsv2rgb import *

def save_ply(ply_path, vertices, faces):

    with open(ply_path, mode='w') as f:

        line = 'ply\n'
        f.write(line)

        line = 'format ascii 1.0\n'
        f.write(line)

        line = 'element vertex %d\n' % len(vertices)
        f.write(line)

        line = 'property float x\n'
        f.write(line)

        line = 'property float y\n'
        f.write(line)

        line = 'property float z\n'
        f.write(line)

        line = 'property uchar red\n'
        f.write(line)

        line = 'property uchar green\n'
        f.write(line)

        line = 'property uchar blue\n'
        f.write(line)

        line = 'element face %d\n' % len(faces)
        f.write(line)

        line = 'property list uchar int vertex_indices\n'
        f.write(line)

        line = 'end_header\n'
        f.write(line)

        for vertex in vertices:
            f.write(vertex)

        for face in faces:
            f.write(face)

def rotDeg2D(p, degree):

    rad = np.deg2rad(degree)
    x = p[0]
    y = p[1]

    X = np.cos(rad) * x - np.sin(rad) * y
    Y = np.sin(rad) * x + np.sin(rad) * y

    return (X, Y)

def createColors(num):

    colors = np.empty((num, 3), np.int32)

    delta = 360 // num

    s = 200
    v = 200

    for i in range(num):

        h = i * delta

        r, g, b = hsv2rgb(h, s, v)

        colors[i] = (b, g, r)

    return colors

def createTetrahedron(size):

    points = np.zeros((4,3), np.float32)
    faces = np.zeros((4,3), np.int32)

    points[0] = ( size, size, size)
    points[1] = (-size,-size, size)
    points[2] = ( size,-size,-size)
    points[3] = (-size, size,-size)

    faces[0] = ( 0, 1, 2)
    faces[1] = ( 1, 3, 2)
    faces[2] = ( 2, 3, 0)
    faces[3] = ( 0, 3, 1)

    colors = createColors(4)

    v = []
    f = []

    for i in range(4):
        for j in range(3):
            idx = faces[i][j]
            line = '%f %f %f %d %d %d\n' % (points[idx][0], points[idx][1], points[idx][2], colors[i][0], colors[i][1], colors[i][2])
            
            v.append(line)

        line = '3 %d %d %d\n' % (i*3+0, i*3+1, i*3+2)
        f.append(line)
        
    return v, f

def main():

    v, f = createTetrahedron(1.0)

    dst_path = 'tetrahedron.ply'
    save_ply(dst_path, v, f)
    print('save %s' % dst_path)


if __name__ == "__main__":
    main()
