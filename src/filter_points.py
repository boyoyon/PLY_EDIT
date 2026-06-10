import numpy as np
import open3d as o3d

def filter_points(points, mode):

    filtered = None

    _points = np.array(points)

    if mode == 'x':
        filtered = _points[_points[:,0] < 0].tolist()
    elif mode == '-x':
        filtered = _points[_points[:,0] > 0].tolist()
    elif mode == 'y':
        filtered = _points[_points[:,1] < 0].tolist()
    elif mode == '-y':
        filtered = _points[_points[:,1] > 0].tolist()
    elif mode == 'z':
        filtered = _points[_points[:,2] < 0].tolist()
    elif mode == '-z':
        filtered = _points[_points[:,2] > 0].tolist()

    return filtered

def mirror_points(points, mode):

    mirrored = None

    _points = np.array(points)

    if mode == 'x':
        filtered = _points[_points[:,0] > 0]
        inverted = filtered.copy()
        inverted[:,0] *= -1
        inverted = inverted[:][::-1]

        mirrored = np.concatenate([filtered, inverted], axis=0).tolist()

    elif mode == '-x':
        filtered = _points[_points[:,0] < 0]
        inverted = filtered.copy()
        inverted[:,0] *= -1
        inverted = inverted[:][::-1]

        mirrored = np.concatenate([filtered, inverted], axis=0).tolist()

    if mode == 'y':
        filtered = _points[_points[:,1] > 0]
        inverted = filtered.copy()
        inverted[:,1] *= -1
        inverted = inverted[:][::-1]

        mirrored = np.concatenate([filtered, inverted], axis=0).tolist()

    if mode == '-y':
        filtered = _points[_points[:,1] < 0]
        inverted = filtered.copy()
        inverted[:,1] *= -1
        inverted = inverted[:][::-1]

        mirrored = np.concatenate([filtered, inverted], axis=0).tolist()

    if mode == 'z':
        filtered = _points[_points[:,2] > 0]
        inverted = filtered.copy()
        inverted[:,2] *= -1
        inverted = inverted[:][::-1]

        mirrored = np.concatenate([filtered, inverted], axis=0).tolist()

    if mode == '-z':
        filtered = _points[_points[:,2] < 0]
        inverted = filtered.copy()
        inverted[:,2] *= -1
        inverted = inverted[:][::-1]

        mirrored = np.concatenate([filtered, inverted], axis=0).tolist()

    return mirrored    
