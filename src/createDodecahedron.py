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

        colors[i] = (r, g, b)

    return colors

def rotDeg2D(p, degree):

    rad = np.deg2rad(degree)
    x = p[0]
    y = p[1]

    X = np.cos(rad) * x - np.sin(rad) * y
    Y = np.sin(rad) * x + np.sin(rad) * y

    return (X, Y)

def createDodecahedron(size):

    points = np.zeros((20, 3), np.float32)
    faces = np.zeros((12,5), np.int32)
    
    P = (size, 0.0)
    z = (np.sqrt(5) + 3) * size / 4
    
    for i in range(5):
        Q = rotDeg2D(P, 18 + 72 * i)
        points[i] = (Q[0], Q[1], z)

    P = ((np.sqrt(5) + 1) * size / 2, 0.0)
    z = (np.sqrt(5) - 1) * size / 4

    for i in range(5, 10):
        Q = rotDeg2D(P, 18 + 72 * i)
        points[i] = (Q[0], Q[1], z)

    z = -(np.sqrt(5) - 1) * size / 4

    for i in range(10, 15):
        Q = rotDeg2D(P, 54 + 72 * i)
        points[i] = (Q[0], Q[1], z)

    P = (size, 0.0)
    z = -(np.sqrt(5) + 3) * size / 4

    for i in range(15, 20):
        Q = rotDeg2D(P, 54 + 72 * i)
        points[i] = (Q[0], Q[1], z)

    faces[0] = ( 5,10, 6, 1, 0)
    faces[1] = ( 3, 4, 0, 1, 2)
    faces[2] = ( 9,14, 5, 0, 4)
    faces[3] = (19,15,10, 5,14)
    faces[4] = (16,11, 6,10,15)
    faces[5] = ( 7, 2, 1,6,11)
    faces[6] = (17,18,13, 8,12)
    faces[7] = (11,16,17,12, 7)
    faces[8] = (15,19,18,17,16)
    faces[9] = (14, 9,13,18,19)
    faces[10] = ( 4, 3, 8,13, 9)
    faces[11] = ( 2, 7,12, 8, 3)
    
    colors = createColors(12)

    v = []
    f = []

    for i in range(12):
        for j in range(5):
            idx = faces[i][j]
            line = '%f %f %f %d %d %d\n' % (points[idx][0], points[idx][1], points[idx][2], colors[i][0], colors[i][1], colors[i][2])
            
            v.append(line)

        line = '5 %d %d %d %d %d\n' % (i*5+0, i*5+1, i*5+2, i*5+3, i*5+4)
        f.append(line)
        
    return v, f

def main():

    v, f = createDodecahedron(1.0)

    dst_path = 'dodecahedron.ply'
    save_ply(dst_path, v, f)
    print('save %s' % dst_path)

if __name__ == "__main__":
    main()
