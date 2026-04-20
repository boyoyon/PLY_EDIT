import numpy as np

def get_rotate_coordinate(x, y, Cx, Cy, theta=np.pi/2):
    newx = x*np.cos(theta)-y*np.sin(theta)+Cx-Cx*np.cos(theta)+Cy*np.sin(theta)
    newz = x*np.sin(theta)+y*np.cos(theta)+Cy-Cx*np.sin(theta)-Cy*np.cos(theta)
    return newx, newz

def dragon1(order, x, z):
    points = []
    points.append((0.0, 0.0, 0.0))
    points.append((x, 0.0, z))

    for depth in range(order):
        for k in range(2**depth):
            newx, newz = get_rotate_coordinate(points[2**depth-k-1][0], points[2**depth-k-1][2], Cx = points[2**depth][0], Cy = points[2**depth][2])
            points.append((newx, 0.0, newz))

    return points
