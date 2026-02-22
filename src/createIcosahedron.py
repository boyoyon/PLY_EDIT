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

    colors = np.empty((num, 3), np.int32)

    delta = 360 // num

    s = 200
    v = 200

    for i in range(num):

        h = i * delta

        r, g, b = hsv2rgb(h, s, v)

        colors[i] = (b, g, r)

    return colors

def rotDeg2D(p, degree):

    rad = np.deg2rad(degree)
    x = p[0]
    y = p[1]

    X = np.cos(rad) * x - np.sin(rad) * y
    Y = np.sin(rad) * x + np.sin(rad) * y

    return (X, Y)

def createIcosahedron(size):

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
        for j in range(3):
            idx = faces[i][j]
            line = '%f %f %f %d %d %d\n' % (points[idx][0], points[idx][1], points[idx][2], colors[i][0], colors[i][1], colors[i][2])
            
            v.append(line)

        line = '3 %d %d %d\n' % (i*3+0, i*3+1, i*3+2)
        f.append(line)
        
    return v, f

def main():

    v, f = createIcosahedron(1.0)

    dst_path = 'icosahedron.ply'
    save_ply(dst_path, v, f)
    print('save %s' % dst_path)


if __name__ == "__main__":
    main()
