import numpy as np
import open3d as o3d
import copy
#from polygon import get_rotation_to_vector

def rotate_points_by_axes(points, new_x, new_y):
    x_axis = new_x / np.linalg.norm(new_x)
    
    y_axis = new_y - np.dot(new_y, x_axis) * x_axis
    y_axis = y_axis / np.linalg.norm(y_axis)
    
    z_axis = np.cross(x_axis, y_axis)
    
    R = np.column_stack((x_axis, y_axis, z_axis))
    
    rotated_points = np.dot(points, R.T)
    
    return rotated_points

def p_polyline(points, section):

    p2 = []
    nr_points = len(points)

    if nr_points > 1 and len(section) > 0:

        if np.array(section).ndim == 3:
            _section0 = np.array(section[-1])
        else:
            _section0 = np.array(section)   

        # x軸向きになるように回転
        R0 = o3d.geometry.get_rotation_matrix_from_xyz((0, 0, np.pi/2)) 
        _section0 = _section0 @ R0.T   

        # パイプの作成 

        prevYaxis = None

        for i in range(1, nr_points-1):

            A = np.array(points[i-1])
            B = np.array(points[i])
            C = np.array(points[i+1])        

            y_axis = np.cross(C-B,B-A)
            y_scale = np.clip(np.linalg.norm(y_axis),0,1) ** 2
 
            if prevYaxis is not None:            
                y_axis = (1 - y_scale) * prevYaxis + y_scale * y_axis

            X_AXIS = B - A

            rotated = rotate_points_by_axes(_section0, X_AXIS, y_axis)
 
            if i == 1:
                p2.append(rotated + A)

            p2.append(rotated + B)

            if i == nr_points - 2:
                p2.append(rotated + C)

            prevYaxis = y_axis

    return p2

