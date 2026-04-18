import numpy as np
import open3d as o3d

"""
filter_points

 mode  0: filter out points x > 0
 mode  1:                   x < 0
 mode  2:                   y > 0
 mode  3:                   y < 0
 mode  4:                   z > 0
 mode  5:                   z < 0

"""

def filter_points(points, mode):

    filtered = None

    points = np.array(points)

    if points is None:
        print('points is None')

    elif mode < 0 or mode > 5:
        print('invalid mode(%d)' % mode)

    else:

        if mode == 0:
            filtered = points[points[:,0] < 0]
        elif mode == 1:
            filtered = points[points[:,0] > 0]
        elif mode == 2:
            filtered = points[points[:,1] < 0]
        elif mode == 3:
            filtered = points[points[:,1] > 0]
        elif mode == 4:
            filtered = points[points[:,2] < 0]
        elif mode == 5:
            filtered = points[points[:,2] > 0]

    return filtered.tolist()
