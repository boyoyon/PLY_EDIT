import numpy as np
import open3d as o3d
import copy
from sphere import _sphere

#
# Internal
#

MIN_VALUE = 0.0000001

def rot2D(x, y, angle):

    X = np.cos(angle) * x - np.sin(angle) * y
    Y = np.sin(angle) * x + np.cos(angle) * y

    return X, Y

def getInt3(str1, str2, str3):
    int1 = int(str1)
    int2 = int(str2)
    int3 = int(str3)

    return (int1, int2, int3)

def get_rotation_to_vector(target, source=np.array([1,0,0],np.float64)):

    a = source / np.linalg.norm(source)
    b = target / np.linalg.norm(target)
    
    # 回転軸（外積）と回転角（内積から算出）
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    
    # ベクトルが平行な場合の処理（外積が0になるため）
    if s < 1e-8:
        return np.eye(3) if c > 0 else -np.eye(3) # 同方向なら単位行列、逆方向なら反転

    # 回転ベクトル（軸 * 角度）の作成
    # 角度 θ = atan2(sin, cos)
    theta = np.arctan2(s, c)
    axis_angle = (v / s) * theta
    
    # Open3Dの関数で回転行列を取得
    return o3d.geometry.get_rotation_matrix_from_axis_angle(axis_angle)

def usagePolygon(cmds):
    print('polygon <nr_of_edges(>=3)> [<size> <width>]')
    print('negative width causes extruded polygon without top/bottom surfaces')
    for i in range(len(cmds)):
        print('%s ' % cmds[i], end="")
    print()

def usagePolyline(cmds):
    print('polyline [<nr_of_edges(>=3)> <size> <ratio> <start> <end>]')
    for i in range(len(cmds)):
        print('%s ' % cmds[i], end="")
    print()

#
# api
#

def polygon(cmds, fIntegrate, SurfaceOuter = (128,128,255), SurfaceInner = (200,200,255), LateralOuter = (128, 128, 255) , LateralInner = (200,200,255)):

    meshes = []
    names = []

    if len(cmds) < 2:
        usagePolygon(cmds)
        return meshes, names

    else:
        nr_divs = int(cmds[1])
        if nr_divs < 3:
            usagePolygon(cmds)
            return meshes, names

        size = 1.0

        if len(cmds) > 2:
            try:
                size = float(eval(cmds[2]))
            except NameError:
                usagePolygon(cmds)
                return meshes, names

        width = 0
        
        if len(cmds) > 3:
            try:
                width = float(eval(cmds[3]))
            except NameError:
                usagePolygon(cmds)
       
        delta = 0.0

        if len(cmds) > 4:
            try:
                delta = float(eval(cmds[4]))
            except NameError:
                usagePolygon(cmds)

        count = 1
        
        if len(cmds) > 5:
            count = int(cmds[5])

        finalSize = size
 
        if len(cmds) > 6:
            try:
                finalSize = float(eval(cmds[6]))
            except NameError:
                usagePolygon(cmds)

        if fIntegrate:

            _meshes = _polygon(nr_divs, size, width, delta, count, SurfaceOuter, SurfaceInner, LateralOuter, LateralInner, finalSize)

            for i in range(len(_meshes)):
                
                if i == 0:
                    accum = copy.deepcopy(_meshes[i])
                else:
                    accum += copy.deepcopy(_meshes[i])

            meshes.append(accum)
            names.append('POLYGON%d' % nr_divs)

        else:

            meshes = _polygon(nr_divs, size, width, delta, count, SurfaceOuter, SurfaceInner, LateralOuter, LateralInner, finalSize)
    
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

def polyline(cmds, Points, fClose, fPadding = False, SurfaceOuter = (128,128,255), SurfaceInner = (200,200,255), LateralOuter = (128, 128, 255) , LateralInner = (200,200,255), PaddingOuter = (255, 180, 255), PaddingInner = (255, 230, 255)):

    meshes = []
    names = []
    accum = None

    if len(Points) > 1:

        clonePoints = copy.deepcopy(Points)
    
        if len(cmds) > 1:
    
            nr_divs = int(cmds[1])
            if nr_divs < 3:
                usagePolyline(cmds)
                return meshes, names
    
        else:
            nr_divs = 25
    
    
        if len(cmds) > 2:
            try:
                size = float(eval(cmds[2]))
            except NameError:
                usagePolyline(cmds)
                return meshes, names
        else:
            size = 0.02

        if len(cmds) > 3:
            try:
                ratio = float(eval(cmds[3]))
            except NameError:
                usagePolyline(cmds)
                return meshes, names
        else:
            ratio = 1.0

        start = ''
        
        if len(cmds) > 4:
            start = cmds[4]

        end = '';

        if len(cmds) > 5:
            end = cmds[5]
   
        _meshes =  _polyiline(size, nr_divs, ratio, fClose, fPadding, start, end, clonePoints, SurfaceOuter, SurfaceInner, LateralOuter, LateralInner, PaddingOuter, PaddingInner)

    
        for i in range(len(_meshes)):
                    
            if i == 0:
                accum = copy.deepcopy(_meshes[i])
            else:
                accum += copy.deepcopy(_meshes[i])
    
        if accum is not None:
            meshes.append(accum)
            names.append('POLYLINE%d' % nr_divs)

    else:
        usagePolyline(cmds)

    return meshes, names

#
# implementation
#

def _polygon(nr_divs, size, width, delta, count, SurfaceOuter, SurfaceInner, LateralOuter, LateralInner, finalSize):

    fgc = np.array(SurfaceOuter)
    bgc = np.array(SurfaceInner)
    sfc = np.array(LateralOuter)
    sbc = np.array(LateralInner)

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
    if width < 0 or finalSize != size:
        fSideOnly = True

        if width < 0:
            width *= -1

    meshes = []

    # create polygon vertices

    num1 = nr_divs * count + 1

    vertTop = np.zeros((num1, 3), np.float64)
    vertSide = np.zeros((num1 * 2, 3), np.float64)

    step = (size - finalSize) / nr_divs / count

    for i in range(nr_divs * count + 1):
        
        if finalSize != size:
            x0 = size - step * i

        angle = stepAngle * i + startAngle
        x, z = rot2D(x0, z0, angle)
        vertTop[i] = [x,y0 + delta * i / nr_divs + width/2, z]
        
        vertSide[i*2]   = [x,y0 + delta * i / nr_divs + width/2, z]
        vertSide[i*2+1] = [x,y0 + delta * i / nr_divs - width/2, z]

    # create Side Mesh

    if width > 0:

        num2 = nr_divs * count * 2

        faceSideFront = np.zeros((num2, 3), np.int32)
        faceSideBack = np.zeros((num2, 3), np.int32)
    
        colSideFront = np.tile(sfc, (num1 * 2, 1))
        colSideBack = np.tile(sbc, (num1 * 2, 1))
   
        for i in range(nr_divs * count):
    
            j = i*2
            k = j + 1
            l = (i+1) * 2
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

    if not fSideOnly and delta == 0: 

        faceTopFront = np.zeros((nr_divs - 2, 3), np.int32)
        faceTopBack = np.zeros((nr_divs - 2, 3), np.int32)
    
        colTopFront = np.tile(fgc, (num1, 1))
        colTopBack = np.tile(bgc, (num1, 1))

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
   
            T = np.array([[1, 0, 0, 0],
                          [0, 1, 0, -width],
                          [0, 0, 1, 0],
                          [0, 0, 0, 1]], np.float64) 
    
            meshBottom.transform(T)
    
            triangles = np.array(meshBottom.triangles)
            meshBottom.triangles = o3d.utility.Vector3iVector(triangles[:,[0,2,1]])
    
            meshes.append(meshBottom)

    return meshes

def _polyiline(size, nr_divs, ratio, fClose, fPadding, start, end, points, SurfaceOuter, SurfaceInner, LateralOuter, LateralInner, PaddingOuter, PaddingInner):

    meshes = []
    accum = None

    if len(points) > 1:

        # y軸向き
        pipe0 = _polygon(nr_divs, size, 1, 0, 1, SurfaceOuter, SurfaceInner, LateralOuter, LateralInner, size)[0]
    
        # x軸向きになるように回転
        R0 = o3d.geometry.get_rotation_matrix_from_xyz((0, 0, np.pi/2)) 
        pipe0.rotate(R0, center=(0,0,0))
   
        nr_points = np.unique(np.array(points), axis=0).shape[0]

        if fClose:
            if len(points) > nr_points:
                points[nr_points] = points[0] # ユニークなデータの後に最初のデータを付加
            else:
                points.append(points[0])

            nr_points += 1
 
        for i in range(1, nr_points):
            A = np.array(points[i-1])
            B = np.array(points[i])
            M = (A + B) * 0.5  
            
            l = np.linalg.norm(B - A)
 
            S = np.array([[l * ratio, 0, 0, 0],
                          [0, 1, 0, 0],
                          [0, 0, 1, 0],
                          [0, 0, 0, 1]],np.float64)
       
            pipe = copy.deepcopy(pipe0)
            pipe.transform(S) 
        
            R = get_rotation_to_vector(B - A) # pipe direction
            if not np.allclose(R,-np.eye(3), atol=1e-8):
                pipe.rotate(R, center=(0,0,0))
        
            T = np.array([[1, 0, 0, M[0]],
                          [0, 1, 0, M[1]],
                          [0, 0, 1, M[2]],
                          [0, 0, 0, 1]], np.float64)
        
            pipe.transform(T)
    
            if i == 1:
                accum = copy.deepcopy(pipe)
            else:
                accum += copy.deepcopy(pipe)
             
            if fPadding:
   
                if i < nr_points - 1:
     
                    C = np.array(points[i+1])
        
                    l2 = np.linalg.norm(C-B)

                    if l2 < MIN_VALUE:
                        continue

                    dot_BA_CB = np.dot(B-A, C-B)
                    cos_theta = dot_BA_CB / (l * l2)
                    theta = np.arccos(np.clip(cos_theta, -1.0, 1.0))
                
                    elevation = [0, np.pi, nr_divs]
        
                    azimuth = [0, theta, nr_divs]
       
                    joint, _ = _sphere(size, elevation, azimuth, PaddingOuter, PaddingInner)
                    JOINT = copy.deepcopy(joint[0])
        
                    R2 = o3d.geometry.get_rotation_matrix_from_xyz((0, np.pi, 0)) 
                    JOINT.rotate(R2, center=(0,0,0))
                    
                    y_axis = np.array([0.0, 1.0, 0.0])
                    Y_AXIS = np.cross(C-B, B-A)
         
                    R3 = get_rotation_to_vector(Y_AXIS, y_axis)
                    if np.allclose(R3,-np.eye(3), atol=1e-8):
                        print('R3 == -eye(3)')
                        R3 = o3d.geometry.get_rotation_matrix_from_xyz((np.pi, 0, 0)) 
                    JOINT.rotate(R3, center=(0,0,0))
        
                    x_axis = R3 @ np.array([1.0, 0.0, 0.0])
                    X_AXIS = B - A
        
                    R4 = get_rotation_to_vector(X_AXIS, x_axis)
                    JOINT.rotate(R4, center=(0,0,0))
                    
                    if np.allclose(R4,-np.eye(3), atol=1e-8):
                        print('R4 == -eye(3)')
                        _triangles = np.asarray(JOINT.triangles)[:,[0,2,1]]
                        JOINT.triangles = o3d.utility.Vector3iVector(_triangles)
                
                    T2 = np.array([[1, 0, 0, B[0]],
                                   [0, 1, 0, B[1]],
                                   [0, 0, 1, B[2]],
                                   [0, 0, 0, 1]], np.float64)
        
                    JOINT.transform(T2)              # move pipe end
        
                    accum += copy.deepcopy(JOINT)   
            
                    if start == 'sphere' and i == 1:
    
                        azimuth = [0, np.pi, nr_divs]
                        joint, _ = _sphere(size, elevation, azimuth, PaddingOuter, PaddingInner)
        
                        START = joint[0]
         
                        T3 = np.array([[1, 0, 0, -l/2],
                                       [0, 1, 0, 0],
                                       [0, 0, 1, 0],
                                       [0, 0, 0, 1]], np.float64)
                        
                        START.transform(T3)              # move pipe start
                        START.rotate(R, center=(0,0,0))  # rotate along the direction of line segment
                        START.transform(T)               # move to the location of line segment
                        accum += copy.deepcopy(START)
    
                if end == 'sphere' and i == nr_points - 1:

                    azimuth = [0, np.pi, nr_divs]
                    elevation = [0, np.pi, nr_divs]
        
                    joint, _ = _sphere(size, elevation, azimuth, PaddingOuter, PaddingInner)
    
                    END = joint[0]
     
                    R2 = o3d.geometry.get_rotation_matrix_from_xyz((0, np.pi, 0)) 
                    
                    END.rotate(R2, center=(0,0,0))

                    T3 = np.array([[1, 0, 0, l/2],
                                   [0, 1, 0, 0],
                                   [0, 0, 1, 0],
                                   [0, 0, 0, 1]], np.float64)
    
                    END.transform(T3)              # move pipe end
                    END.rotate(R, center=(0,0,0))  # rotate along the direction of line segment
                    END.transform(T)               # move to the location of line segment
                    accum += copy.deepcopy(END)
    
        if accum is not None:
            meshes.append(accum)

    return meshes
