import numpy as np
import open3d as o3d
import copy

#
# Internal
#

def rot2D(x, y, angle):

    X = np.cos(angle) * x - np.sin(angle) * y
    Y = np.sin(angle) * x + np.cos(angle) * y

    return X, Y

def getInt3(str1, str2, str3):
    int1 = int(str1)
    int2 = int(str2)
    int3 = int(str3)

    return (int1, int2, int3)

def usage(cmds):
    print('polygon <nr_of_edges(>=3)> [<size> <width>]')
    print('negative width causes extruded polygon without side faces')
    for i in range(len(cmds)):
        print('%s ' % cmds[i], end="")
#
# api
#

def polygon(cmds, fIntegrate):

    meshes = []
    names = []

    if len(cmds) < 2:
        usage(cmds)
        return meshes, names

    else:
        nr_divs = int(cmds[1])
        if nr_divs < 3:
            usage(cmds)
            return meshes, names

        size = 1.0

        if len(cmds) > 2:
            try:
                size = float(eval(cmds[2]))
            except NameError:
                usage(cmds)
                return meshes, names

        width = 0
        
        if len(cmds) > 3:
            try:
                width = float(eval(cmds[3]))
            except NameError:
                usage(cmds)
        
        front = (128, 128, 255)
        back = (200,200,255)

        sideFront = (128,128,196)
        sideBack = (200,200,255)

        if fIntegrate:

            _meshes = _polygon(nr_divs, size, width, front, back, sideFront, sideBack)

            for i in range(len(_meshes)):
                
                if i == 0:
                    accum = copy.deepcopy(_meshes[i])
                else:
                    accum += copy.deepcopy(_meshes[i])

            meshes.append(accum)
            names.append('POLYGON%d' % nr_divs)

        else:

            meshes = _polygon(nr_divs, size, width, front, back, sideFront, sideBack)
    
            names = []
    
            if len(meshes) > 0:
                if np.abs(width) > 0:
                    names.append('polygon%d_side' % nr_divs)
                else:
                    names.append('polygon%d_top' % nr_divs)
    
            if len(meshes) > 1:
                names.append('polygon%d_top' % nr_divs)
    
            if len(meshes) > 2:
                names.append('polygon%d_bottom' % nr_divs)

    return meshes, names

#
# implementation
#

def _polygon(nr_divs, size, width, front, back, sideFront, sideBack):

    fgc = np.array(front)
    bgc = np.array(back)
    sfc = np.array(sideFront)
    sbc = np.array(sideBack)

    fgc = fgc.astype(np.float64) / 255.0
    bgc = bgc.astype(np.float64) / 255.0
    sfc = sfc.astype(np.float64) / 255.0
    sbc = sbc.astype(np.float64) / 255.0

    x0 = size
    y0 = 0.0
    z0 = 0.0

    stepAngle = np.pi * 2 / nr_divs
    startAngle = stepAngle / 2

    fSideOnly = False
    if width < 0:
        fSideOnly = True
        width *= -1

    meshes = []

    # create polygon vertices

    vertTop = np.zeros((nr_divs, 3), np.float64)

    colTopFront = np.tile(fgc, (nr_divs, 1))
    colTopBack = np.tile(bgc, (nr_divs, 1))

    for i in range(nr_divs):
        
        angle = stepAngle * i + startAngle
        x, z = rot2D(x0, z0, angle)
        vertTop[i]=[x,y0+width/2,z]

    # create Side Mesh

    if width > 0:

        vertSide = np.zeros((nr_divs * 2, 3), np.float64)
        faceSideFront = np.zeros((nr_divs * 2, 3), np.int32)
        faceSideBack = np.zeros((nr_divs * 2, 3), np.int32)
    
        colSideFront = np.tile(fgc, (nr_divs * 2, 1))
        colSideBack = np.tile(bgc, (nr_divs * 2, 1))
    
        for i in range(len(vertTop)):
    
            vertSide[i*2] = vertTop[i]
            vertSide[i*2+1] = vertTop[i]
            vertSide[i*2+1][1] *= -1
    
            j = i*2
            k = j + 1
            l = ((i+1) % nr_divs) * 2
            m = l + 1
    
            faceSideFront[i*2] = (j, l, k)
            faceSideFront[i*2+1] = (l, m, k) 
    
            faceSideBack[i*2] = (j, k, l)
            faceSideBack[i*2+1] = (l, k, m) 
    
        meshSideFront = o3d.geometry.TriangleMesh()
        meshSideFront.vertices = o3d.utility.Vector3dVector(vertSide)
        meshSideFront.triangles = o3d.utility.Vector3iVector(faceSideFront)
        meshSideFront.vertex_colors = o3d.utility.Vector3dVector(colSideFront)
    
        meshSideBack = o3d.geometry.TriangleMesh()
        meshSideBack.vertices = o3d.utility.Vector3dVector(vertSide)
        meshSideBack.triangles = o3d.utility.Vector3iVector(faceSideBack)
        meshSideBack.vertex_colors = o3d.utility.Vector3dVector(colSideBack)
    
        meshSide = meshSideFront + meshSideBack
    
        meshes.append(meshSide)
    
    # create top surface

    if not fSideOnly: 

        faceTopFront = np.zeros((nr_divs - 2, 3), np.int32)
        faceTopBack = np.zeros((nr_divs - 2, 3), np.int32)
    
        colTopFront = np.tile(fgc, (nr_divs, 1))
        colTopBack = np.tile(bgc, (nr_divs, 1))

        for i in range(2, nr_divs):
    
            faceTopFront[i-2] = [0,i,i-1]
            faceTopBack[i-2] = [0,i-1,i]
    
        meshTopFront = o3d.geometry.TriangleMesh()
        meshTopFront.vertices = o3d.utility.Vector3dVector(vertTop)
        meshTopFront.triangles = o3d.utility.Vector3iVector(faceTopFront)
        meshTopFront.vertex_colors = o3d.utility.Vector3dVector(colTopFront)
    
        meshTopBack = o3d.geometry.TriangleMesh()
        meshTopBack.vertices = o3d.utility.Vector3dVector(vertTop)
        meshTopBack.triangles = o3d.utility.Vector3iVector(faceTopBack)
        meshTopBack.vertex_colors = o3d.utility.Vector3dVector(colTopBack)
    
        meshTop = meshTopFront + meshTopBack
    
        meshes.append(meshTop)

        if width > 0:
    
            # create bottom surface
            meshBottom = copy.deepcopy(meshTop)
    
            flipY = np.eye(4)
            flipY[1][1] = -1
    
            meshBottom.transform(flipY)
    
            # vertex はflip するが面は裏返しにならないので裏返す
            triangles = np.array(meshBottom.triangles)
            meshBottom.triangles = o3d.utility.Vector3iVector(triangles[:,[0,2,1]])
    
            meshes.append(meshBottom)

    return meshes
