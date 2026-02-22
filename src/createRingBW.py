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

def createRingBW(NR_DIVS, size, width):

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

        line = '%f %f %f 0 0 0\n' % (x - width / 2, y, z)
        verticesRing.append(line)

        line = '%f %f %f 0 0 0\n' % (x + width / 2, y, z)
        verticesRing.append(line)

        if i > 0:
            n = i * 2
            line = '3 %d %d %d\n' % (n - 1, n - 2, n + 1)
            facesRing.append(line)

            line = '3 %d %d %d\n' % (n - 2, n, n + 1)
            facesRing.append(line)

            if i % 2 == 1:
            
                line = '3 %d %d %d\n' % (n - 2, n - 1, n + 1)
                facesRing.append(line)

                line = '3 %d %d %d\n' % (n, n - 2, n + 1)
                facesRing.append(line)
 

    return verticesRing, facesRing

def main():

    argv = sys.argv
    argc = len(argv)

    print('%s creates black and white ring' % argv[0])
    print('[usage] python %s <no. of vertices> <size> <width>' % argv[0])

    nr_vertices = 100

    if argc > 1:
        nr_vertices = int(argv[1])

    size = 1.0

    if argc > 2:
        size = float(argv[2])

    width = 0.01

    if argc > 3:
        width = float(argv[3])

    vertices, faces = createRingBW(100, 1, 0.01)

    dst_path = 'ringBW_%d.ply' % nr_vertices
    save_ply(dst_path, vertices, faces)

    print('save %s' % dst_path)

if __name__ == '__main__':
    main()
