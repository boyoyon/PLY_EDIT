import numpy as np

def wrap2cylinder(points, mode, mode2, radius, extra):
    
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]

    if mode == 'xy':

        width = points[-1][0] - points[0][0] + (points[1][0] - points[0][0]) * extra
        min_value = points[0][0]
        theta = ((x - min_value) / width) * (2 * np.pi)

        if mode2 == 'vert':

            new_x = radius * np.cos(theta)
            new_z = radius * np.sin(theta)
            new_y = y

        elif mode2 == 'horz':

            deltaR = y - np.min(y)

            new_x = (radius + deltaR) * np.cos(theta)
            new_y = (radius + deltaR) * np.sin(theta)
            new_z = z

        else:
            return None   
    
    elif mode == 'xz':

        width = points[-1][0] - points[0][0] + (points[1][0] - points[0][0]) * extra
        min_value = points[0][0]
        theta = ((x - min_value) / width) * (2 * np.pi)

        if mode2 == 'vert':

            new_x = radius * np.cos(theta)
            new_y = radius * np.sin(theta)
            new_z = z

        elif mode2 == 'horz':

            deltaR = z - np.min(z)

            new_x = (radius + deltaR) * np.cos(theta)
            new_z = (radius + deltaR) * np.sin(theta)
            new_y = y

        else:
            return None   
    
    
    elif mode == 'yx':

        width = points[-1][1] - points[0][1] + (points[1][1] - points[0][1]) * extra
        min_value = points[0][1]
        theta = ((y - min_value) / width) * (2 * np.pi)

        if mode2 == 'vert':

            new_y = radius * np.cos(theta)
            new_z = radius * np.sin(theta)
            new_x = x

        elif mode2 == 'horz':

            deltaR = x - np.min(x)

            new_y = (radius + deltaR) * np.cos(theta)
            new_x = (radius + deltaR) * np.sin(theta)
            new_z = z

        else:
            return None   
    
    
    elif mode == 'yz':

        width = points[-1][1] - points[0][1] + (points[1][1] - points[0][1]) * extra
        min_value = points[0][1]
        theta = ((y - min_value) / width) * (2 * np.pi)

        if mode2 == 'vert':

            new_y = radius * np.cos(theta)
            new_x = radius * np.sin(theta)
            new_z = z

        elif mode2 == 'horz':

            deltaR = z - np.min(z)

            new_y = (radius + deltaR) * np.cos(theta)
            new_z = (radius + deltaR) * np.sin(theta)
            new_x = x

        else:
            return None   
    
    
    elif mode == 'zx':

        width = points[-1][2] - points[0][2] + (points[1][2] - points[0][2]) * extra
        min_value = points[0][2]
        theta = ((z - min_value) / width) * (2 * np.pi)

        if mode2 == 'vert':

            new_z = radius * np.cos(theta)
            new_y = radius * np.sin(theta)
            new_x = x

        elif mode2 == 'horz':

            deltaR = x - np.min(x)

            new_z = (radius + deltaR) * np.cos(theta)
            new_x = (radius + deltaR) * np.sin(theta)
            new_y = y

        else:
            return None   
    
    
    elif mode == 'zy':

        width = points[-1][2] - points[0][2] + (points[1][2] - points[0][2]) * extra
        min_value = points[0][2]
        theta = ((z - min_value) / width) * (2 * np.pi)

        if mode2 == 'vert':

            new_z = radius * np.cos(theta)
            new_x = radius * np.sin(theta)
            new_y = y

        elif mode2 == 'horz':

            deltaR = y - np.min(y)

            new_z = (radius + deltaR) * np.cos(theta)
            new_y = (radius + deltaR) * np.sin(theta)
            new_x = x

        else:
            return None   
    
    else:
        return None

    return np.column_stack((new_x, new_y, new_z))

