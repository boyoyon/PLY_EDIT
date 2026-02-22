import sys
import numpy as np

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

        #line = 'property list uchar int vertex_index\n'
        line = 'property list uchar int vertex_indices\n'
        f.write(line)

        line = 'end_header\n'
        f.write(line)

        for vertex in vertices:
            f.write(vertex)

        for face in faces:
            f.write(face)

def createRing(NR_DIVS, size, width, fgc, bgc):

    x0 = 0.0
    y0 = size
    z0 = 0.0
    
    verticesRing = []
    facesRing = []

    angleStep = np.pi * 2 / NR_DIVS

    x = x0
    y = y0
    z = z0

    for i in range(NR_DIVS + 1):

        angle = angleStep * i

        x = x0
        y = np.cos(angle) * y0 - np.sin(angle) * z0
        z = np.sin(angle) * y0 + np.cos(angle) * z0

        line = '%f %f %f %d %d %d\n' % (x - width / 2, y, z, fgc[0], fgc[1], fgc[2])
        verticesRing.append(line)

        line = '%f %f %f %d %d %d\n' % (x + width / 2, y, z, fgc[0], fgc[1], fgc[2])
        verticesRing.append(line)

        line = '%f %f %f %d %d %d\n' % (x - width / 2, y, z, bgc[0], bgc[1], bgc[2])
        verticesRing.append(line)

        line = '%f %f %f %d %d %d\n' % (x + width / 2, y, z, bgc[0], bgc[1], bgc[2])
        verticesRing.append(line)

        if i > 0:
            n = i * 4
            line = '3 %d %d %d\n' % (n - 3, n - 4, n + 1)
            facesRing.append(line)

            line = '3 %d %d %d\n' % (n - 4, n, n + 1)
            facesRing.append(line)

            line = '3 %d %d %d\n' % (n - 2, n - 1, n + 3)
            facesRing.append(line)

            line = '3 %d %d %d\n' % (n - 2, n + 3, n + 2)
            facesRing.append(line)

    return verticesRing, facesRing

def main():

    fgc = [  0,   0, 255]
    bgc = [200, 200, 255]

    argv = sys.argv
    argc = len(argv)

    print('%s creates ring ply' % argv[0])
    print('[usage] python %s <no. of vertices> <size> <width> <foreground color(r g b)> <background color(r g b)>' % argv[0])

    nr_vertices = 100

    if argc > 1:
        nr_vertices = int(argv[1])

    size = 1.0

    if argc > 2:
        size = float(argv[2])

    width = 0.01

    if argc > 3:
        width = float(argv[3])

    if argc > 4:
        fgc[0] = int(argv[4])

    if argc > 5:
        fgc[1] = int(argv[5])

    if argc > 6:
        fgc[2] = int(argv[6])

    if argc > 7:
        bgc[0] = int(argv[7])

    if argc > 8:
        bgc[1] = int(argv[8])

    if argc > 9:
        bgc[2] = int(argv[9])

    vertices, faces = createRing(nr_vertices, size, width, fgc, bgc)

    dst_path = 'ring_%d.ply' % nr_vertices

    save_ply(dst_path, vertices, faces)

    print('save %s' % dst_path)

if __name__ == '__main__':
    main()
