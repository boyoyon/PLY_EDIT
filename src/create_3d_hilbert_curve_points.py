# pip install numpy-hilbert-curve

import numpy as np
from hilbert import decode
import sys

def create_3d_hilbert_curve_points(bitsNumber):

    dimension = 3
    max_hilbert_integer = 2 ** (bitsNumber * dimension)

    hilbert_integers = np.arange(max_hilbert_integer)
    points = decode(hilbert_integers, dimension, bitsNumber)/bitsNumber

    dst_path = '3d_hilbert_curve_points_%dbits.npy' % bitsNumber
    np.save(dst_path, points)
    print('save %s' % dst_path)

def main():

    argv = sys.argv
    argc = len(argv)

    print('%s cretes 3d hilbert curve points' % argv[0])
    print('[usage] python %s <bitsNumber(1/2/3/4/5)>' % argv[0])

    if argc < 2:
        quit()

    create_3d_hilbert_curve_points(int(argv[1]))

if __name__ == '__main__':
    main()