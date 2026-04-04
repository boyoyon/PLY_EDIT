import numpy as np
import open3d as o3d
import copy

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

            self.points = _points + self.pos
            self.points0 = _points

        else:
            self.points = self.pos[np.newaxis,:] # points:(1,3)
            self.points0 = np.array((0.0, 0.0, 0.0))[np.newaxis,:] # points:(1,3)

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
            self.p2.append(copy.deepcopy(self.points)) # p2:list of (m,3)

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

        offset = self.head * length
        self.pos += offset
        self.points = self.points0 @ self.R.T
        self.points += self.pos

        if self.pen:
            self.p2.append(copy.deepcopy(self.points)) # if pen is down, append points to p2

    def turn(self, pitch, yaw, roll):
        _radPitch  = np.deg2rad(pitch)
        _radYaw   = np.deg2rad(yaw)
        _radRoll = np.deg2rad(roll)

        _R = o3d.geometry.get_rotation_matrix_from_xyz((_radPitch, _radYaw, _radRoll))

        #self.R = _R @ self.R
        self.R = self.R @ _R
        
        axisZ = np.array((0.0, 0.0, 1.0))
        self.head = self.R @ axisZ

    def getP2(self):
        return self.p2
