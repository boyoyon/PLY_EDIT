import numpy as np
import open3d as o3d
import copy
from polygon import get_rotation_to_vector

def p_polyline(points, section):

    p2 = []
    nr_points = len(points)

    if nr_points > 1 and len(section) > 0:

        if len(np.array(section)) == 3:
            _section0 = np.array(section[-1])
        else:
            _section0 = np.array(section)   

        # x軸向きになるように回転
        R0 = o3d.geometry.get_rotation_matrix_from_xyz((0, 0, np.pi/2)) 
        _section0 = _section0 @ R0.T   
 
        _sectionA = _section0
        _sectionB = _section0

        # パイプの作成 
        for i in range(1, nr_points-1):

            A = np.array(points[i-1])
            B = np.array(points[i])
            C = np.array(points[i+1])        

            y_axis = np.array([0.0, 1.0, 0.0])
            Y_AXIS = np.cross(C-B, B-A)
     
            R3 = get_rotation_to_vector(Y_AXIS, y_axis)
                
            if np.allclose(R3,-np.eye(3), atol=1e-8):
                print('R3 nearly equals -np.eye(3)')
                R3 = o3d.geometry.get_rotation_matrix_from_xyz((np.pi, 0, 0)) 
                #R3 = -np.eye(3)

            x_axis = R3 @ np.array([1.0, 0.0, 0.0])
            X_AXIS = B - A
 
            R4 = get_rotation_to_vector(X_AXIS, x_axis)
            if np.allclose(R4,-np.eye(3), atol=1e-8):
                print('R4 nearly equal -np.eye(3)')
                R4 = -np.eye(3)

            R = R4

            if i == 1:
                p2.append(_section0 @ R.T + A)

            p2.append(_section0 @ R.T + B)

            if i == nr_points - 2:
                p2.append(_section0 @ R.T + C)

    return p2

