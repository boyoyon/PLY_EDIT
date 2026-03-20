import numpy as np
import open3d as o3d

def surface(p2, layer1, layer2, fPathClose, fNearest, start, end, outer, inner):

    _meshes = []
    _names = []

    if layer1 is None or layer2 is None:
        print('layer is None')
        return _meshes, _names    

    nr1 = len(p2[layer1])
    nr2 = len(p2[layer2])

    if nr1 == 0 or nr2 == 0:
        print('layer has no point')
        return _meshes, _names

    if end < 0:
        end += (nr1 + 1)
    else:
        end += 1

    _triangles = []
    points = np.array(p2[layer1] + p2[layer2])
  
    if not fNearest: # connect points with the same index

        #for i in range(nr1):
        for i in range(start, end):

            j = (i + 1) % nr1

            #if not fPathClose and i == end - 1:
            if not fPathClose and i == nr1 - 1:
                break

            idx0 = i
            idx1 = i + nr1
            idx2 = j
            idx3 = j + nr1

            _triangles.append((idx0, idx1, idx2))
            _triangles.append((idx1, idx3, idx2))
 
    else: # connect point with the nearest point

        _nearest = []
  
        #for i in range(start, end):
        for i in range(nr1):

            _work = []

            for j in range(nr2):

                _p1 = np.array(p2[layer1][i])
                _p2 = np.array(p2[layer2][j])
                _work.append(np.linalg.norm(_p1 - _p2))

            _nearest.append(np.argmin(np.array(_work)))
        
        #for i in range(start, end):
        for i in range(nr1):

            j = (i + 1) % nr1

            idx0 = i
            idx1 = _nearest[i] + nr1
            idx2 = j
            idx3 = _nearest[j] + nr1

            _triangles.append((idx0, idx1, idx2))
            _triangles.append((idx1, idx3, idx2))

    if len(_triangles) > 0:

        _triangles = np.array(_triangles)
    
        outer = np.array(outer).astype(np.float64) / 255.0
        OUTER = np.tile(outer, (nr1+nr2, 1))
    
        _meshOuter = o3d.geometry.TriangleMesh()
        _meshOuter.vertices = o3d.utility.Vector3dVector(points)
        _meshOuter.triangles = o3d.utility.Vector3iVector(_triangles)
        _meshOuter.vertex_colors = o3d.utility.Vector3dVector(OUTER)
     
        _triangles_inner = _triangles[:,[0,2,1]]
    
        inner = np.array(inner).astype(np.float64) / 255.0
        INNER = np.tile(inner, (nr1+nr2, 1))
    
        _meshInner = o3d.geometry.TriangleMesh()
        _meshInner.vertices = o3d.utility.Vector3dVector(points)
        _meshInner.triangles = o3d.utility.Vector3iVector(_triangles_inner)
        _meshInner.vertex_colors = o3d.utility.Vector3dVector(INNER)

        _meshes.append(_meshOuter + _meshInner)
        _names.append('ring_%d_%d' % (layer1, layer2))

    return _meshes, _names
 

