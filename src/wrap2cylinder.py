import numpy as np

def pwrap(points, mode, radius, extra):
    
    _points = np.array(points)
    
    x = _points[:, 0]
    y = _points[:, 1]
    z = _points[:, 2]

    _width_x = np.max(_points[:,0])-np.min(_points[:,0])
    _width_y = np.max(_points[:,1])-np.min(_points[:,1])
    _width_z = np.max(_points[:,2])-np.min(_points[:,2])

    _width_max = np.max([_width_x, _width_y, _width_z])
    _width_min = np.min([_width_x, _width_y, _width_z])

    mode2 = ''

    if _width_x == _width_max:

        if _width_y == _width_min:
            mode2 = 'xz'
        else:
            mode2 = 'xy'

    elif _width_y == _width_max:

        if _width_x == _width_min:
            mode2 = 'yz'
        else:
            mode2 = 'yx'

    elif _width_z == _width_max:
 
        if _width_x == _width_min:
            mode2 = 'zy'
        else:
            mode2 = 'zx'

    print(mode2)

    if mode2 == 'xy':

        width = points[-1][0] - points[0][0] + (points[1][0] - points[0][0]) * extra
        min_value = points[0][0]
        theta = ((x - min_value) / width) * (2 * np.pi)

        if mode == 'vert':

            new_x = radius * np.cos(theta)
            new_z = radius * np.sin(theta)
            new_y = y

        elif mode == 'horz':

            deltaR = y - np.min(y)

            new_x = (radius + deltaR) * np.cos(theta)
            new_y = (radius + deltaR) * np.sin(theta)
            new_z = z

        else:
            return None   
    
    elif mode2 == 'xz':

        width = points[-1][0] - points[0][0] + (points[1][0] - points[0][0]) * extra
        min_value = points[0][0]
        theta = ((x - min_value) / width) * (2 * np.pi)

        if mode == 'vert':

            new_x = radius * np.cos(theta)
            new_y = radius * np.sin(theta)
            new_z = z

        elif mode == 'horz':

            deltaR = z - np.min(z)

            new_x = (radius + deltaR) * np.cos(theta)
            new_z = (radius + deltaR) * np.sin(theta)
            new_y = y

        else:
            return None   
    
    
    elif mode2 == 'yx':

        width = points[-1][1] - points[0][1] + (points[1][1] - points[0][1]) * extra
        min_value = points[0][1]
        theta = ((y - min_value) / width) * (2 * np.pi)

        if mode == 'vert':

            new_y = radius * np.cos(theta)
            new_z = radius * np.sin(theta)
            new_x = x

        elif mode == 'horz':

            deltaR = x - np.min(x)

            new_y = (radius + deltaR) * np.cos(theta)
            new_x = (radius + deltaR) * np.sin(theta)
            new_z = z

        else:
            return None   
    
    
    elif mode2 == 'yz':

        width = points[-1][1] - points[0][1] + (points[1][1] - points[0][1]) * extra
        min_value = points[0][1]
        theta = ((y - min_value) / width) * (2 * np.pi)

        if mode == 'vert':

            new_y = radius * np.cos(theta)
            new_x = radius * np.sin(theta)
            new_z = z

        elif mode == 'horz':

            deltaR = z - np.min(z)

            new_y = (radius + deltaR) * np.cos(theta)
            new_z = (radius + deltaR) * np.sin(theta)
            new_x = x

        else:
            return None   
    
    
    elif mode2 == 'zx':

        width = points[-1][2] - points[0][2] + (points[1][2] - points[0][2]) * extra
        min_value = points[0][2]
        theta = ((z - min_value) / width) * (2 * np.pi)

        if mode == 'vert':

            new_z = radius * np.cos(theta)
            new_y = radius * np.sin(theta)
            new_x = x

        elif mode == 'horz':

            deltaR = x - np.min(x)

            new_z = (radius + deltaR) * np.cos(theta)
            new_x = (radius + deltaR) * np.sin(theta)
            new_y = y

        else:
            return None   
    
    
    elif mode2 == 'zy':

        width = points[-1][2] - points[0][2] + (points[1][2] - points[0][2]) * extra
        min_value = points[0][2]
        theta = ((z - min_value) / width) * (2 * np.pi)

        if mode == 'vert':

            new_z = radius * np.cos(theta)
            new_x = radius * np.sin(theta)
            new_y = y

        elif mode == 'horz':

            deltaR = y - np.min(y)

            new_z = (radius + deltaR) * np.cos(theta)
            new_y = (radius + deltaR) * np.sin(theta)
            new_x = x

        else:
            return None   
    
    else:
        return None

    return np.column_stack((new_x, new_y, new_z))

def p2wrap(p2, mode, radius, extra):

    if mode != 'vert' and mode != 'horz':
        return None

    _p2 = np.array(p2)
    print('_p2.shape', _p2.shape)
    _c = np.mean(_p2, axis=1)  
    print('_c.shape', _c.shape)

    _width_x = np.max(_c[:,0])-np.min(_c[:,0])
    _width_y = np.max(_c[:,1])-np.min(_c[:,1])
    _width_z = np.max(_c[:,2])-np.min(_c[:,2])

    _width_max = np.max([_width_x, _width_y, _width_z])
    _width_min = np.min([_width_x, _width_y, _width_z])

    mode2 = ''

    if _width_x == _width_max:

        if _width_y == _width_min:
            mode2 = 'xz'
        else:
            mode2 = 'xy'

    elif _width_y == _width_max:

        if _width_x == _width_min:
            mode2 = 'yz'
        else:
            mode2 = 'yx'

    elif _width_z == _width_max:
 
        if _width_x == _width_min:
            mode2 = 'zy'
        else:
            mode2 = 'zx'

    new_p2 = []

    if mode2 == 'xy':

        width = _c[-1][0] - _c[0][0] + (_c[1][0] - _c[0][0]) * extra
        min_value = _c[0][0]

        for i in range(_p2.shape[0]):

            x = _p2[i,:,0] - _c[i,0]
            y = _p2[i,:,1] - _c[i,1]
            z = _p2[i,:,2] - _c[i,2]

            theta = ((_c[i,0] - min_value) / width) * (2 * np.pi)
    
            if mode == 'vert':
    
                new_x = (x + radius) * np.cos(theta) 
                new_z = (z + radius) * np.sin(theta)
                new_y = y
    
            elif mode == 'horz':
    
                deltaR = y - np.min(y)
    
                new_x = (radius + deltaR) * np.cos(theta)
                new_y = (radius + deltaR) * np.sin(theta)
                new_z = z
    
            new_p2.append(np.column_stack((new_x, new_y, new_z)))

    elif mode2 == 'xz':

        width = _c[-1][0] - _c[0][0] + (_c[1][0] - _c[0][0]) * extra
        min_value = _c[0][0]

        for i in range(_p2.shape[0]):

            x = _p2[i,:,0] - _c[i,0]
            y = _p2[i,:,1] - _c[i,1]
            z = _p2[i,:,2] - _c[i,2]

            theta = ((_c[i,0] - min_value) / width) * (2 * np.pi)
    
            if mode == 'vert':
    
                new_x = (x + radius) * np.cos(theta)
                new_y = (y + radius) * np.sin(theta)
                new_z = z
    
            elif mode == 'horz':
    
                deltaR = z - np.min(z)
    
                new_x = (radius + deltaR) * np.cos(theta)
                new_z = (radius + deltaR) * np.sin(theta)
                new_y = y
    
            new_p2.append(np.column_stack((new_x, new_y, new_z)))
    
    elif mode2 == 'yx':

        width = _c[-1][1] - _c[0][1] + (_c[1][1] - _c[0][1]) * extra
        min_value = _c[0][1]

        for i in range(_p2.shape[0]):

            x = _p2[i,:,0] - _c[i,0]
            y = _p2[i,:,1] - _c[i,1]
            z = _p2[i,:,2] - _c[i,2]

            theta = ((_c[i,1] - min_value) / width) * (2 * np.pi)
    
            if mode == 'vert':
    
                new_y = (y + radius) * np.cos(theta)
                new_z = (z + radius) * np.sin(theta)
                new_x = x
    
            elif mode == 'horz':
    
                deltaR = x - np.min(x)
    
                new_y = (radius + deltaR) * np.cos(theta)
                new_x = (radius + deltaR) * np.sin(theta)
                new_z = z

            new_p2.append(np.column_stack((new_x, new_y, new_z)))
    
    elif mode2 == 'yz':

        width = _c[-1][1] - _c[0][1] + (_c[1][1] - _c[0][1]) * extra
        min_value = _c[0][1]

        for i in range(_p2.shape[0]):

            x = _p2[i,:,0] - _c[i,0]
            y = _p2[i,:,1] - _c[i,1]
            z = _p2[i,:,2] - _c[i,2]

            theta = ((_c[i,1] - min_value) / width) * (2 * np.pi)
    
            if mode == 'vert':
    
                new_y = (y + radius) * np.cos(theta)
                new_x = (x + radius) * np.sin(theta)
                new_z = z
    
            elif mode == 'horz':
    
                deltaR = z - np.min(z)
    
                new_y = (radius + deltaR) * np.cos(theta)
                new_z = (radius + deltaR) * np.sin(theta)
                new_x = x

            new_p2.append(np.column_stack((new_x, new_y, new_z)))
    
    elif mode2 == 'zx':

        width = _c[-1][2] - _c[0][2] + (_c[1][2] - _c[0][2]) * extra
        min_value = _c[0][2]

        for i in range(_p2.shape[0]):

            x = _p2[i,:,0] - _c[i,0]
            y = _p2[i,:,1] - _c[i,1]
            z = _p2[i,:,2] - _c[i,2]

            theta = ((_c[i,2] - min_value) / width) * (2 * np.pi)
    
            if mode == 'vert':
    
                new_z = (z + radius) * np.cos(theta)
                new_y = (y + radius) * np.sin(theta)
                new_x = x
    
            elif mode == 'horz':
    
                deltaR = x - np.min(x)
    
                new_z = (radius + deltaR) * np.cos(theta)
                new_x = (radius + deltaR) * np.sin(theta)
                new_y = y
    
            new_p2.append(np.column_stack((new_x, new_y, new_z)))

    elif mode2 == 'zy':

        width = _c[-1][2] - _c[0][2] + (_c[1][2] - _c[0][2]) * extra
        min_value = _c[0][2]

        for i in range(_p2.shape[0]):

            x = _p2[i,:,0] - _c[i,0]
            y = _p2[i,:,1] - _c[i,1]
            z = _p2[i,:,2] - _c[i,2]

            theta = ((_c[i,2] - min_value) / width) * (2 * np.pi)
    
            if mode == 'vert':
    
                new_z = (z + radius) * np.cos(theta)
                new_x = (x + radius) * np.sin(theta)
                new_y = y
    
            elif mode == 'horz':
    
                deltaR = y - np.min(y)
    
                new_z = (radius + deltaR) * np.cos(theta)
                new_y = (radius + deltaR) * np.sin(theta)
                new_x = x
    
            new_p2.append(np.column_stack((new_x, new_y, new_z)))

    else:
        return None

    return np.array(new_p2)

def p2bend(p2, rotM):

    _p2 = np.array(p2)

    for i in range(1, _p2.shape[0]):

        _p = _p2[i]
        _c = np.mean(_p, axis=0)

        _p2 -= _c

        _part = _p2[0:i]
        _part = _part @ rotM.T
        _p2[0:i] = _part

    return _p2.tolist()
     

