import cv2, glob, os, sys
import numpy as np
import open3d as o3d

def main():

    argv = sys.argv
    argc = len(argv)

    print('%s merges mesh plys' % argv[0])
    print('[usage] python %s <wildcard for mesh plys>' % argv[0])
    print('[usage] python %s <mesh ply1> <mesh ply2> ...' % argv[0])

    if argc < 2:
        quit()

    paths = []

    if argc > 2:
        for i in range(1, argc):
            paths.append(argv[i])

    else:
        paths = glob.glob(argv[1])
    
    mesh = None

    for i, path in enumerate(paths):

        if i == 0:
            mesh =  o3d.io.read_triangle_mesh(path)

        else:
            mesh += o3d.io.read_triangle_mesh(path)

    dst_path = 'merged.ply'

    o3d.io.write_triangle_mesh(dst_path, mesh)
    print('save %s' % dst_path)

if __name__ == '__main__':
    main()
