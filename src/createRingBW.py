import sys
import numpy as np

NR_DIVS = 100

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

def createRingBW(nr_divs, size, width):

    x0 = 0.0
    y0 = size
    z0 = 0.0
    
    vertices = []
    faces = []

    angleStep = np.pi * 2 / nr_divs

    points = []

    for i in range(nr_divs):

        angle = angleStep * i

        x = x0
        y = np.cos(angle) * y0 - np.sin(angle) * z0
        z = np.sin(angle) * y0 + np.cos(angle) * z0

        points.append((x,y,z))
   
    points = np.array(points)
 
    num = NR_DIVS // (nr_divs * 2)

    if num < 1:
        num = 1

    for i in range(nr_divs):

        start = points[i]
        end = points[(i+1) % nr_divs]

        for j in range(num):

            alpha = j / num
            p0 = start * alpha + end * (1 - alpha)
        
            beta = (j+1) / num
            p1 = start * beta + end * (1 - beta)

            p2 = p0 * 0.5 + p1 * 0.5

            line = '%f %f %f 0 0 0\n' % (p0[0] - width / 2, p0[1], p0[2])
            vertices.append(line)

            line = '%f %f %f 0 0 0\n' % (p0[0] + width / 2, p0[1], p0[2])
            vertices.append(line)

            line = '%f %f %f 0 0 0\n' % (p2[0] - width / 2, p2[1], p2[2])
            vertices.append(line)

            line = '%f %f %f 0 0 0\n' % (p2[0] + width / 2, p2[1], p2[2])
            vertices.append(line)

            line = '%f %f %f 0 0 0\n' % (p1[0] - width / 2, p1[1], p1[2])
            vertices.append(line)

            line = '%f %f %f 0 0 0\n' % (p1[0] + width / 2, p1[1], p1[2])
            vertices.append(line)

            n = (i * num + j) * 6 

            line = '4 %d %d %d %d\n' % (n+0,  n+1, n+3, n+2)
            faces.append(line)

            line = '4 %d %d %d %d\n' % (n+2,  n+3, n+5, n+4)
            faces.append(line)

            line = '4 %d %d %d %d\n' % (n+2,  n+3, n+1, n+0)
            faces.append(line)

    return vertices, faces

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

    vertices, faces = createRingBW(nr_vertices, size, width)

    dst_path = 'ringBW_%d.ply' % nr_vertices
    save_ply(dst_path, vertices, faces)

    print('save %s' % dst_path)

if __name__ == '__main__':
    main()
