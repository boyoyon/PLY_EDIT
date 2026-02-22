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

def createColors(num):

    colors = np.empty((num * 2, 3), np.int32)

    delta = 360 // num

    sFront = 200
    vFront = 230

    sBack =  25
    vBack = 240

    for i in range(num):

        j = i * 2
        h = i * delta

        r, g, b = hsv2rgb(h, sFront, vFront)
        colors[j] = (b, g, r)
        
        r, g, b = hsv2rgb(h, sBack, vBack)
        colors[j+1] = (b, g, r)

    return colors

def rotDeg2D(p, degree):

    rad = np.deg2rad(degree)
    x = p[0]
    y = p[1]

    X = np.cos(rad) * x - np.sin(rad) * y
    Y = np.sin(rad) * x + np.sin(rad) * y

    return (X, Y)

def createSoccerball(size):

    points = np.zeros((12, 3), np.float32)
    faces = np.zeros((20, 3), np.int32)

    t = (1+np.sqrt(5)) / 2 * size

    points[0] = ( t, 0,  size)
    points[1] = ( t, 0, -size)
    points[2] = (-t, 0, -size)
    points[3] = (-t, 0,  size)
    
    points[4] = ( size,  t, 0)
    points[5] = (-size,  t, 0)
    points[6] = (-size, -t, 0)
    points[7] = ( size, -t, 0)
    
    points[8] = (0,  size,  t)
    points[9] = (0, -size,  t)
    points[10] = (0, -size, -t)
    points[11] = (0,  size, -t)

    faces[0] = ( 0, 1, 4)
    faces[1] = ( 0, 7, 1)
    faces[2] = ( 0, 9, 7)
    faces[3] = ( 0, 8, 9)
    faces[4] = ( 0, 4, 8)
    faces[5] = (11, 4, 1)
    faces[6] = (10, 1, 7)
    faces[7] = ( 6, 7, 9)
    faces[8] = ( 3, 9, 8)
    faces[9] = ( 5, 8, 4)
    faces[10] = ( 1,10,11)
    faces[11] = ( 7, 6,10)
    faces[12] = ( 9, 3, 6)
    faces[13] = ( 8, 5, 3)
    faces[14] = ( 4,11, 5)
    faces[15] = ( 2,11,10)
    faces[16] = ( 2,10, 6)
    faces[17] = ( 2, 6, 3)
    faces[18] = ( 2, 3, 5)
    faces[19] = ( 2, 5,11)

    colors = createColors(20)

    v = []
    f = []

    for i in range(20):
        idx0 = faces[i][0]
        idx1 = faces[i][1]
        idx2 = faces[i][2]

        p0 = (points[idx0] * 2 + points[idx1] * 1) / 3
        p1 = (points[idx0] * 1 + points[idx1] * 2) / 3
    
        p2 = (points[idx1] * 2 + points[idx2] * 1) / 3
        p3 = (points[idx1] * 1 + points[idx2] * 2) / 3
    
        p4 = (points[idx2] * 2 + points[idx0] * 1) / 3
        p5 = (points[idx2] * 1 + points[idx0] * 2) / 3

        j = i * 2

        line = '%f %f %f %d %d %d\n' % (p0[0], p0[1], p0[2], colors[j][0], colors[j][1], colors[j][2])
        v.append(line)
        line = '%f %f %f %d %d %d\n' % (p1[0], p1[1], p1[2], colors[j][0], colors[j][1], colors[j][2])
        v.append(line)
        line = '%f %f %f %d %d %d\n' % (p2[0], p2[1], p2[2], colors[j][0], colors[j][1], colors[j][2])
        v.append(line)
        line = '%f %f %f %d %d %d\n' % (p3[0], p3[1], p3[2], colors[j][0], colors[j][1], colors[j][2])
        v.append(line)
        line = '%f %f %f %d %d %d\n' % (p4[0], p4[1], p4[2], colors[j][0], colors[j][1], colors[j][2])
        v.append(line)
        line = '%f %f %f %d %d %d\n' % (p5[0], p5[1], p5[2], colors[j][0], colors[j][1], colors[j][2])
        v.append(line)

        line = '%f %f %f %d %d %d\n' % (p0[0], p0[1], p0[2], colors[j+1][0], colors[j+1][1], colors[j+1][2])
        v.append(line)
        line = '%f %f %f %d %d %d\n' % (p1[0], p1[1], p1[2], colors[j+1][0], colors[j+1][1], colors[j+1][2])
        v.append(line)
        line = '%f %f %f %d %d %d\n' % (p2[0], p2[1], p2[2], colors[j+1][0], colors[j+1][1], colors[j+1][2])
        v.append(line)
        line = '%f %f %f %d %d %d\n' % (p3[0], p3[1], p3[2], colors[j+1][0], colors[j+1][1], colors[j+1][2])
        v.append(line)
        line = '%f %f %f %d %d %d\n' % (p4[0], p4[1], p4[2], colors[j+1][0], colors[j+1][1], colors[j+1][2])
        v.append(line)
        line = '%f %f %f %d %d %d\n' % (p5[0], p5[1], p5[2], colors[j+1][0], colors[j+1][1], colors[j+1][2])
        v.append(line)

        line = '6 %d %d %d %d %d %d\n' % (i*12+0, i*12+1, i*12+2, i*12+3, i*12+4, i*12+5)
        f.append(line)
        
        line = '6 %d %d %d %d %d %d\n' % (i*12+11, i*12+10, i*12+9, i*12+8, i*12+7, i*12+6)
        f.append(line)
        
    return v, f

def main():

    v, f = createSoccerball(1.0)

    dst_path = 'soccerball.ply'
    save_ply(dst_path, v, f)
    print('save %s' % dst_path)

if __name__ == "__main__":
    main()
