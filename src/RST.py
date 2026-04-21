import numpy as np
import open3d as o3d
from getValues import Eval, Evals

def usageRotate():
    print('specify angle_x(degree) angle_y(degree) angle_z(degree) [<count(>=2)>]')
                    
def usageScale():  
    print('specify scalee_x scale_y scale_z [<count(>=2)>]')
   
def usageTranslate(): 
    print('specify offset_x offset_y offset_z [<count(>=2)>]')
    
def usageGroup():        
    print('specify group operation (ex. r xx xx xx s xx xx xx t xx xx xx) [<count(>=2)>]')
   
def getRotateMatrix(cmds, size=3):

    if len(cmds) < 3:
        usageRotate()
        return None
                      
    else:

        fResult, values = Evals(cmds, 3)
    
        if fResult:
    
            rad_x = np.deg2rad(values[0])
            rad_y = np.deg2rad(values[1])
            rad_z = np.deg2rad(values[2])
    
            if size == 4:
                R = np.eye(4)
                r = o3d.geometry.get_rotation_matrix_from_xyz((rad_x, rad_y, rad_z))
                R[:3,:3] = r            

            else:
                R = o3d.geometry.get_rotation_matrix_from_xyz((rad_x, rad_y, rad_z))
            return R

        else:
            usageRotate()
            return None
    
def getScaleMatrix(cmds, size=4):
 
    if len(cmds) < 3:
        usageScale()
        return None
                      
    else:

        fResult, values = Evals(cmds, 3)
    
        if fResult:

            if size == 4:    
                S = np.array([[values[0],  0,          0,         0],
                              [ 0,         values[1],  0,         0],
                              [ 0,         0,          values[2], 0],
                              [ 0,         0,          0,         1]])

            else:
                S = np.array([[values[0],  0,          0],
                              [ 0,         values[1],  0],
                              [ 0,         0,          values[2]]])
    
            return S

        else:
            usageScale()
            return None
    
def getTranslateMatrix(cmds, size=4):

    if len(cmds) < 3:
        usageTranslate()
        return None
                      
    else:

        fResult, values = Evals(cmds, 3)
    
        if fResult:
    
            if size == 4:

                T = np.array([[ 1,  0,  0, values[0]],
                              [ 0,  1,  0, values[1]],
                              [ 0,  0,  1, values[2]],
                              [ 0,  0,  0, 1]])

            else:

                T = np.array([values[0], values[1], values[2]])
        
            return T

        else:
            usageTranslate()
            return None
   
def getGroupMatrix(cmds):
 
    if len(cmds) < 3:
        usageGroup()

        return None, None
                      
    else:
        G = np.eye(4)
    
        idx = 0
        fResult = True
    
        while len(cmds) - idx > 3:
    
            if cmds[idx] == 'r' or cmds[idx] == 'R':
    
                r = getRotateMatrix(cmds[idx+1:])  # 3x3

                if r is None:
                    usageGroup()

                    return None, None
         
                R = np.eye(4)
                R[:3,:3] = r
    
                G = G @ R
    
            elif cmds[idx] == 's' or cmds[idx] == 'S':

                S = getScaleMatrix(cmds[idx+1:])

                if S is None:
                    usageGroup()

                    return None, None
    
                G = G @ S
    
            elif cmds[idx] == 't' or cmds[idx] == 'T':
    
                T = getTranslateMatrix(cmds[idx+1:])
 
                if T is None:
                    usageGroup()

                    return None, None
 
                G = G @ T
    
            idx += 4
   
    fRemain = False
    if len(cmds) > idx:
        fRemain = True
 
    return G, fRemain
