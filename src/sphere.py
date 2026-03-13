import numpy as np
import open3d as o3d
import copy
from getValues import Eval, Evals

#
# Inner
#
def rot2D(x0, y0, angle):

    x = np.cos(angle) * x0 - np.sin(angle) * y0
    y = np.sin(angle) * x0 + np.cos(angle) * y0

    return x, y

def usage(cmds):

    print('sphere <size> [<nr_divs> <latitude (start, end)>, <longitude (start, end)> <nr_divs(longitude)>]')

    for i in range(len(cmds)):
        print('%s ' % cmds[i], end="")

#
# API
#

def sphere(cmds, LateralOuter=(128,128,255), LateralInner=(200,200,255)):

    meshes = []
    names = []

    if len(cmds) < 2:
        usage(cmds)
        return meshes, names

    else:

        fResult, value = Eval(cmds[1])
        
        if fResult:
            size = value
        else:
            usage(cmds)
            return meshes, names

        elevation_start = 0
        elevation_end = 180
        elevation_nr_divs = 25

        if len(cmds) > 2:

            if cmds[2].isdecimal():
                elevation_nr_divs = int(cmds[2])
            else:
                usage(cmds)
                return meshes, names

        azimuth_nr_divs = elevation_nr_divs

        if len(cmds) > 4:

           fResult, value = Eval(cmds[3])

           if fResult:
               elevation_start = value
           else:
               usage(cmds)
               return meshes, names

           fResult, value = Eval(cmds[4])

           if fResult:
               elevation_end = value
           else:
               usage(cmds)
               return meshes, names

        azimuth_start = 0
        azimuth_end = 360

        if len(cmds) > 6:

           fResult, value = Eval(cmds[5])

           if fResult:
               azimuth_start = value
           else:
               usage(cmds)
               return meshes, names

           fResult, value = Eval(cmds[6])

           if fResult:
               azimuth_end = value
           else:
               usage(cmds)
               return meshes, names

        elevations = [np.deg2rad(elevation_start), 
            np.deg2rad(elevation_end), elevation_nr_divs]
        
        if len(cmds) > 7 and cmds.isdecimal():
           azimuth_nr_divs = int(cmds[7])

        azimuths = [np.deg2rad(azimuth_start), 
            np.deg2rad(azimuth_end), azimuth_nr_divs]

        meshes, names = _sphere(size, elevations, azimuths, LateralOuter, LateralInner)

    return meshes, names

#
# Implementation
#

def _sphere(size, elevations, azimuths, color_outer, color_inner):

    elevation_nr_divs = elevations[2]
    azimuth_nr_divs = azimuths[2]

    num1 = elevation_nr_divs * azimuth_nr_divs
    num2 = (elevation_nr_divs - 1) * (azimuth_nr_divs - 1) * 2

    points = np.zeros((num1, 3), np.float64)
    faces = np.zeros((num2, 3), np.int32)

    color_outer = np.array(color_outer).astype(np.float64) / 255.0
    color_inner = np.array(color_inner).astype(np.float64) / 255.0

    Couter = np.tile(color_outer, (num1, 1))
    Cinner = np.tile(color_inner, (num1, 1))

    x0 = 0.0
    y0 = size
    z0 = 0.0
        
    for i, elevation in enumerate(np.linspace(elevations[0], elevations[1], elevations[2])):

        y1, z1 = rot2D(y0, z0, elevation)

        for j, azimuth in enumerate(np.linspace(azimuths[0], azimuths[1], azimuths[2])):

            idx = i * azimuth_nr_divs + j 
            x, z = rot2D(x0, z1, azimuth)
            points[idx] = [x, y1, z]

    for i in range(elevation_nr_divs - 1):
        for j in range(azimuth_nr_divs - 1):
        
            idx0 = i * azimuth_nr_divs + j
            idx1 = (i+1) * azimuth_nr_divs + j
            idx2 = idx0 + 1
            idx3 = idx1 + 1
            
            IDX = (i * (azimuth_nr_divs - 1) + j) * 2

            faces[IDX]   = [idx0, idx2, idx1]
            faces[IDX+1] = [idx2, idx3, idx1]

    meshFront = o3d.geometry.TriangleMesh()
    meshFront.vertices = o3d.utility.Vector3dVector(points)
    meshFront.triangles = o3d.utility.Vector3iVector(faces)
    meshFront.vertex_colors = o3d.utility.Vector3dVector(Couter)

    meshBack = o3d.geometry.TriangleMesh()
    meshBack.vertices = o3d.utility.Vector3dVector(points)
    facesBack = copy.deepcopy(faces)
    facesBack = facesBack[:,[0,2,1]]
    meshBack.triangles = o3d.utility.Vector3iVector(facesBack)
    meshBack.vertex_colors = o3d.utility.Vector3dVector(Cinner)

    meshes = []
    names = []

    meshes.append(meshFront + meshBack)
    names.append('sphere')

    return meshes, names 
