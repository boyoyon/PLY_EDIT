import numpy as np
import open3d as o3d
import copy
from sphere import _sphere
from getValues import Eval, Evals

#
# Internal
#

MIN_VALUE = 0.0000001

def rot2D(x, y, angle):

    X = np.cos(angle) * x - np.sin(angle) * y
    Y = np.sin(angle) * x + np.cos(angle) * y

    return X, Y

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

def usagePolygonBorder(cmds):
    print('polygon_border <nr_of_edges(>=3)> [<size> <width>]')
    for i in range(len(cmds)):
        print('%s ' % cmds[i], end="")
    print()

def usagePolyline(cmds):
    print('polyline [<nr_of_edges(>=3)> <size> <ratio> <start> <end>]')
    for i in range(len(cmds)):
        print('%s ' % cmds[i], end="")
    print()

def usageStar(cmds):
    print('star size [depth]')
    for i in range(len(cmds)):
        print('%s ' % cmds[i], end="")
    print()

#
# api
#

def polygon(cmds, fIntegrate, SurfaceOuter = (128,128,255), SurfaceInner = (200,200,255), LateralOuter = (128, 128, 255) , LateralInner = (200,200,255), side = 'both'):

    meshes = []
    names = []

    if len(cmds) < 2:
        usagePolygon(cmds)
        return meshes, names

    else:
        if not cmds[1].isdecimal():
            usagePolygon(cmds)
            return meshes, names
        
        else:
            nr_divs = int(cmds[1])
        
        if nr_divs < 3:
            usagePolygon(cmds)
            return meshes, names

        size = 1.0

        if len(cmds) > 2:

            fResult, value = Eval(cmds[2])

            if fResult:
                size = value
            else:
                usagePolygon(cmds)
                return meshes, names

        width = 0
        
        if len(cmds) > 3:

            fResult, value = Eval(cmds[3])

            if fResult:
                width = value
            else:
                usagePolygon(cmds)
       
        delta = 0.0

        if len(cmds) > 4:

            fResult, value = Eval(cmds[4])

            if fResult:
                delta = value
            else:
                usagePolygon(cmds)

        count = 1
        
        if len(cmds) > 5 and cmds[5].isdecimal():
            count = int(cmds[5])

            if not cmds[5].isdecimal():
                usagePolygon(cmds)

        finalSize = size
 
        if len(cmds) > 6:

            fResult, value = Eval(cmds[6])

            if fResult:
                finalSize = value
            else:
                usagePolygon(cmds)

        if fIntegrate:

            _meshes = _polygon(nr_divs, size, width, delta, count, SurfaceOuter, SurfaceInner, LateralOuter, LateralInner, finalSize, side)

            for i in range(len(_meshes)):
                
                if i == 0:
                    accum = copy.deepcopy(_meshes[i])
                else:
                    accum += copy.deepcopy(_meshes[i])

            meshes.append(accum)
            names.append('POLYGON%d' % nr_divs)

        else:

            meshes = _polygon(nr_divs, size, width, delta, count, SurfaceOuter, SurfaceInner, LateralOuter, LateralInner, finalSize, side)
    
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

def polygon_border(cmds, SurfaceOuter = (128,128,255), SurfaceInner = (200,200,255)):

    meshes = []
    names = []

    if len(cmds) < 4:
        usagePolygonBorder(cmds)
        return meshes, names

    else:
        if not cmds[1].isdecimal():
            usagePolygonBorder(cmds)
            return meshes, names
        
        else:
            nr_divs = int(cmds[1])
        
        if nr_divs < 3:
            usagePolygonBorder(cmds)
            return meshes, names

        size = 1.0

        if len(cmds) > 2:

            fResult, value = Eval(cmds[2])

            if fResult:
                size = value
            else:
                usagePolygonBorder(cmds)
                return meshes, names

        width = 0
        
        if len(cmds) > 3:

            fResult, value = Eval(cmds[3])

            if fResult:
                width = value
            else:
                usagePolygonBorder(cmds)
       
        front_color = SurfaceOuter
        back_color = SurfaceInner

        if len(cmds) > 6:
            fRsult, values = Evals(cmds[4:], 3)

            if fResult:
                front_color = copy.deepcopy(values)

                if len(cmds) > 9:
                    fResult, values = Evals(cmds[7:],3)
                    
                    if fResult:
                        back_color = copy.deepcopy(values)

        _meshes = _polygon_border(nr_divs, size, width, front_color, back_color)

        accum = None
        for i in range(len(_meshes)):
            
            if i == 0:
                accum = copy.deepcopy(_meshes[i])
            else:
                accum += copy.deepcopy(_meshes[i])

        meshes.append(accum)
        names.append('polygon_border%d' % nr_divs)

    return meshes, names

def polyline(cmds, Points, fClose, fPadding = False, SurfaceOuter = (128,128,255), SurfaceInner = (200,200,255), LateralOuter = (128, 128, 255) , LateralInner = (200,200,255), PaddingOuter = (255, 180, 255), PaddingInner = (255, 230, 255)):

    meshes = []
    names = []
    accum = None

    if len(Points) > 1:

        clonePoints = copy.deepcopy(Points)
    
        if len(cmds) > 1:
   
            if not cmds[1].isdecimal():
                usagePolyline(cmds)
                return meshes, names

            else: 
                nr_divs = int(cmds[1])

            if nr_divs < 3:
                usagePolyline(cmds)
                return meshes, names
    
        else:
            nr_divs = 25
    
    
        if len(cmds) > 2:

            fResult, value = Eval(cmds[2])

            if fResult:
                size = value
            else:
                usagePolyline(cmds)
                return meshes, names
        else:
            size = 0.02

        if len(cmds) > 3:

            fResult, value = Eval(cmds[3])

            if fResult:
                ratio = value
            else:
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
   
        _meshes =  _polyline(size, nr_divs, ratio, fClose, fPadding, start, end, clonePoints, SurfaceOuter, SurfaceInner, LateralOuter, LateralInner, PaddingOuter, PaddingInner)

    
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

def star(cmds, SurfaceOuter, SurfaceInner, LateralOuter, LateralInner):

    _meshes = []
    _names = []

    size = -1

    if len(cmds) > 1:
        fResult, value = Eval(cmds[1])
    
        if fResult:
           size = value
    
        else:
            usageStar(cmds)
            return _meshes, _names
    else:
        usageStar(cmds)
        return _meshes, _names   
 
    depth = size / 2
    
    if len(cmds) > 2:

        fResult, value = Eval(cmds[2])
    
        if fResult:
           depth = value
    
        else:
            usageStar(cmds)
            return _meshes, _names
 
    red = 230
    green = 255
    blue = 64

    values = (red, green, blue)

    if len(cmds) > 5:

        fResult, values = Evals(cmds[3:], 3)
    
        if not fResult:
            usageStar(cmds)
            return _meshes, _names
 
    _meshes = _star(size, depth, values)   
    _names.append('star')

    return _meshes, _names 

#
# implementation
#

def _polygon(nr_divs, size, width, delta, count, SurfaceOuter, SurfaceInner, LateralOuter, LateralInner, finalSize, side):

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
   
        if side == 'sideA': 
            meshSide = meshSideFront

        elif side == 'sideAA':
            meshSide = meshSideBack

        else:
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
   
        if side == 'sideA': 
            meshTop = meshTopFront

        elif side == 'sideAA':
            meshTop = meshTopBack

        else:
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

def _polygon_border(nr_divs, size, width, SurfaceOuter, SurfaceInner):

    x0 = size
    y0 = 0.0
    z0 = 0.0

    stepAngle = np.pi * 2 / nr_divs
    startAngle = stepAngle / 2

    meshes = []

    # create polygon_border vertices

    vertLarge = []
    vertSmall = []

    x0Large = size
    x0Small = size - width
    y0 = 0.0
    z0 = 0.0

    stepAngle = np.pi * 2 / nr_divs
    startAngle = stepAngle / 2

    for i in range(nr_divs):

        angle = stepAngle * i + startAngle
        xLarge, zLarge = rot2D(x0Large, z0, angle)
        vertLarge.append([xLarge, y0, zLarge])
        
        xSmall, zSmall = rot2D(x0Small, z0, angle)
        vertSmall.append([xSmall, y0, zSmall])

    vertices = np.array(vertLarge + vertSmall)

    # create Meshes

    trianglesFront = []
    trianglesBack = []
    
    for i in range(nr_divs):
   
        j = (i + 1) % nr_divs
 
        idx0 = i
        idx1 = j
        idx2 = idx0 + nr_divs
        idx3 = idx1 + nr_divs
 
        trianglesFront.append([idx0, idx2, idx1])   
        trianglesFront.append([idx2, idx3, idx1])   
    
        trianglesBack.append([idx0, idx1, idx2])   
        trianglesBack.append([idx2, idx1, idx3])   
  
    trianglesFront = np.array(trianglesFront)
    trianglesBack = np.array(trianglesBack)
 
    fgc = np.array(SurfaceOuter).astype(np.float64) / 255.0
    bgc = np.array(SurfaceInner).astype(np.float64) / 255.0
 
    colorsFront = np.tile(fgc, (nr_divs * 2, 1))
    colorsBack = np.tile(bgc, (nr_divs * 2, 1))

    meshFront = o3d.geometry.TriangleMesh()
    meshFront.vertices = o3d.utility.Vector3dVector(vertices)
    meshFront.triangles = o3d.utility.Vector3iVector(trianglesFront)
    meshFront.vertex_colors = o3d.utility.Vector3dVector(colorsFront)
    
    meshBack = o3d.geometry.TriangleMesh()
    meshBack.vertices = o3d.utility.Vector3dVector(vertices)
    meshBack.triangles = o3d.utility.Vector3iVector(trianglesBack)
    meshBack.vertex_colors = o3d.utility.Vector3dVector(colorsBack)
  
    meshes.append(meshFront + meshBack)
    
    return meshes

def _polyline(size, nr_divs, ratio, fClose, fPadding, start, end, points, SurfaceOuter, SurfaceInner, LateralOuter, LateralInner, PaddingOuter, PaddingInner):

    meshes = []
    accum = None

    if len(points) > 1:

        # y軸向き
        pipe0 = _polygon(nr_divs, size, 1, 0, 1, SurfaceOuter, SurfaceInner, LateralOuter, LateralInner, size)[0]
    
        # x軸向きになるように回転
        R0 = o3d.geometry.get_rotation_matrix_from_xyz((0, 0, np.pi/2)) 
        pipe0.rotate(R0, center=(0,0,0))
   
        # 頂点が重複している場合がある
        nr_points = np.unique(np.array(points), axis=0).shape[0]

        # パイプの作成 
        for i in range(0, nr_points):

            # 線分の終点側でパイプを作成する。not fClose の場合i==0 はスキップ
            if not fClose and i == 0:
                continue

            if i == 0:
                _prev= nr_points - 1
            else:
                _prev = i - 1

            A = np.array(points[_prev])
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
    
            if accum is None:
                accum = copy.deepcopy(pipe)
            else:
                accum += copy.deepcopy(pipe)
           
            # not fClose で最初の点と最後の点に球指定があった場合の対応 
            if not fClose and fPadding:

                azimuth = [0, np.pi, nr_divs]
                elevation = [0, np.pi, nr_divs]

                if (start == 'sphere' or start == '-sphere') and i == 1:

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

                    if start == '-sphere':
                        _triangles = np.asarray(START.triangles)[:,[0,2,1]]
                        START.triangles = o3d.utility.Vector3iVector(_triangles)

                    accum += copy.deepcopy(START)

                if (end == 'sphere' or end == '-sphere') and i == nr_points - 1:
        
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

                    if end == '-sphere':
                        _triangles = np.asarray(END.triangles)[:,[0,2,1]]
                        END.triangles = o3d.utility.Vector3iVector(_triangles)

                    accum += copy.deepcopy(END)

            # パディングの作成。A → B → C の並びのB で実施 
            if fPadding and nr_points > 2:
   
                _next = i + 1

                # 最終ポイントの場合, C は最初の点
                if i == nr_points - 1:
                   
                    if not fClose:
                        continue

                    _next = 0
 
                C = np.array(points[_next])
    
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
                    R3 = o3d.geometry.get_rotation_matrix_from_xyz((np.pi, 0, 0)) 
                
                JOINT.rotate(R3, center=(0,0,0))
    
                x_axis = R3 @ np.array([1.0, 0.0, 0.0])
                X_AXIS = B - A
    
                R4 = get_rotation_to_vector(X_AXIS, x_axis)
                JOINT.rotate(R4, center=(0,0,0))
               
                if np.allclose(R4,-np.eye(3), atol=1e-8):
                    _triangles = np.asarray(JOINT.triangles)[:,[0,2,1]]
                    JOINT.triangles = o3d.utility.Vector3iVector(_triangles)

                T2 = np.array([[1, 0, 0, B[0]],
                               [0, 1, 0, B[1]],
                               [0, 0, 1, B[2]],
                               [0, 0, 0, 1]], np.float64)
    
                JOINT.transform(T2)              # move pipe end
    
                accum += copy.deepcopy(JOINT)   
    
        if accum is not None:
            meshes.append(accum)

    return meshes

def _star(size, depth, rgb):

    _meshes = []

    # calculate outer pentagon's vertices
    p0 = []
    angle = np.pi * 2 / 5
    y0 = -size
    z0 = 0

    for i in range(5):
        a = angle * i + angle / 2
        y = np.cos(a) * y0 - np.sin(a) * z0
        z = np.sin(a) * y0 + np.cos(a) * z0
        p0.append((0, y, z))

    # calculate inner pentagon's vertices
    p1 = []
    p2 = []
    angle = -np.pi * 2 / 10
    scale = np.cos(np.pi * 2/5) / np.cos(np.pi * 2/10)

    for i in range(5):
        y = np.cos(angle) * p0[i][1] - np.sin(angle) * p0[i][2]
        z = np.sin(angle) * p0[i][1] + np.cos(angle) * p0[i][2]
        p1.append((depth/4, y * scale, z * scale))
        p2.append((-depth/4, y * scale, z * scale))

    p3 = []
    p3.append((depth/2, 0.0, 0.0)) # 15
    p3.append((-depth/2, 0.0, 0.0)) # 16

    points = np.array(p0 + p1 + p2 + p3)

    triangles1 = []
    triangles2 = []
    triangles3 = []
    triangles4 = []
    triangles5 = []
    triangles6 = []

    for i in range(5):

        idx0 = i
        idx1 = i + 5
        idx2 = (i + 1) % 5 + 5

        idx3 = i + 10
        idx4 = (i + 1) % 5 + 10

        triangles1.append((idx0, 15, idx1))
        triangles2.append((idx2, 15, idx0))

        triangles3.append((idx0, idx3, 16))
        triangles4.append((idx4, idx0, 16))
    
        triangles5.append((idx0, idx1, idx3))
        triangles6.append((idx0, idx4, idx2))

    trianglesFront = np.array(triangles1 + triangles2)    
    trianglesBack  = np.array(triangles3 + triangles4)    
    trianglesSide  = np.array(triangles5 + triangles6)   
 
    rgb = np.array(rgb).astype(np.float64) / 255.0
    outerColors = np.tile(rgb, (points.shape[0], 1))

    meshFront = o3d.geometry.TriangleMesh()
    meshFront.vertices = o3d.utility.Vector3dVector(points)
    meshFront.triangles = o3d.utility.Vector3iVector(trianglesFront)
    meshFront.vertex_colors = o3d.utility.Vector3dVector(outerColors)

    meshBack = o3d.geometry.TriangleMesh()
    meshBack.vertices = o3d.utility.Vector3dVector(points)
    meshBack.triangles = o3d.utility.Vector3iVector(trianglesBack)
    meshBack.vertex_colors = o3d.utility.Vector3dVector(outerColors)

    meshSide = o3d.geometry.TriangleMesh()
    meshSide.vertices = o3d.utility.Vector3dVector(points)
    meshSide.triangles = o3d.utility.Vector3iVector(trianglesSide)
    meshSide.vertex_colors = o3d.utility.Vector3dVector(outerColors)

    mesh = meshFront + meshBack + meshSide

    _meshes.append(mesh)

    meshContour = o3d.geometry.TriangleMesh()
    meshContour.vertices = o3d.utility.Vector3dVector(points[:5])

    _meshes.append(meshContour)

    return _meshes 
