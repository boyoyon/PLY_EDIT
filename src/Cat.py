import numpy as np
import open3d as o3d
import copy

SCALE = 0.1

def _head2R(head):

    axisZ = np.array((0.0, 0.0, 1.0))
    R = None

    if np.allclose(axisZ, head): # 向きの変更なし
        R = np.eye(3)
    elif np.allclose(axisZ, -head): # 反対向き(y軸周りに180°回転)
        R = o3d.geometry.get_rotation_matrix_from_xyz((0.0, np.pi, 0))
    else:
        v = np.cross(axisZ, head)
        c = np.dot(axisZ, head)
        vx = np.array([[    0, -v[2], v[1]],
                       [ v[2],    0, -v[0]], 
                       [-v[1],  v[0],   0]])

        R = np.eye(3) + vx + np.matmul(vx,vx)*((1-c)/(np.linalg.norm(v)**2))

    return R

class Cat():

    def __init__(self, pen, pos, head, points):
        self.pos = np.array(pos).astype(np.float64) # pos:(3,)

        if len(points) > 0:
            _points = np.array(points).astype(np.float64)

            _mean = np.mean(_points)
            _points += (self.pos - _mean)

            self.points = _points * SCALE # points:(m,3)

        else:
            self.points = self.pos[np.newaxis,:] # points:(1,3)

        _head = np.array(head) # head:(3,)
        _head_l = np.linalg.norm(_head)

        if _head_l < 1e-6:
            self.head = np.array((0.0, 0.0, 1.0))
            self.R = np.eye(3)
        else:
            self.head = _head / _head_l
            self.R = _head2R(self.head)

        self.pen  = pen
        self.p2   = []
        self.p3   = []    
 
        if pen:
            self.p2.append(self.points) # p2:list of (m,3)

    def isPenDown(self):
        return self.pen

    def getPos(self):
        return self.pos

    def setPos(self, pos):
        self.pos = np.array(pos).astype(np.float64)

    def getHead(self):
        return self.head

    def setHead(self, head):
        _head = np.array(head) # head:(3,)
        _head_l = np.linalg.norm(_head)

        if _head_l < 1e-6:
            self.head = np.array((0.0, 0.0, 1.0))
            self.R = np.eye(3)
        else:
            self.head = _head / _head_l
            self.R = _head2R(self.head)

    def pen(self, updown):
        _prev = self.pen

        if _prev == True and updown == False: # pen up
            self.p3.append(self.p2) # p3: list of (list of (m,3))
            self.p2.clear()
      
        if _prev == False and updown == True: # pen down

            self.p2.clear()
            self.p2.append(self.points)

        self.pen = updown

    def f(self, length):

        length *= SCALE
        offset = self.head * length
        self.pos += offset

        OFFSET = np.tile(offset,(self.points.shape[0], 1))       
        self.points += OFFSET * SCALE
        #self.points += offset

        if self.pen:
            self.p2.append(self.points) # if pen is down, append points to p2

    def turn(self, roll, yaw, pitch):
        _radRoll  = np.deg2rad(roll)
        _radYaw   = np.deg2rad(yaw)
        _radPitch = np.deg2rad(pitch)

        _R = o3d.geometry.get_rotation_matrix_from_xyz((_radRoll, _radYaw, _radPitch))

        self.R = _R @ self.R
        
        axisZ = np.array((0.0, 0.0, 1.0))
        self.head = self.R @ axisZ
