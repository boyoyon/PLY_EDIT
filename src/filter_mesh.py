import numpy as np
import open3d as o3d

"""
filter_mesh

 mode  0: filter out triangels including x > 0
 mode  1:                                x < 0
 mode  2:                                y > 0
 mode  3:                                y < 0
 mode  4:                                z > 0
 mode  5:                                z < 0

 mode  6:                      all vertices x > 0
 mode  7:                                   x < 0
 mode  8:                                   y > 0
 mode  9:                                   y < 0
 mode 10:                                   z > 0
 mode 11:                                   z < 0

"""

def filter0(vertices, triangles):

    filtered = []
    for t in triangles:
        idx = t[0]
        if vertices[idx][0] > 0:
            continue
        idx = t[1]
        if vertices[idx][0] > 0:
            continue
        idx = t[2]
        if vertices[idx][0] > 0:
            continue
        filtered.append(t)

    return filtered

def filter1(vertices, triangles):

    filtered = []
    for t in triangles:
        idx = t[0]
        if vertices[idx][0] < 0:
            continue
        idx = t[1]
        if vertices[idx][0] < 0:
            continue
        idx = t[2]
        if vertices[idx][0] < 0:
            continue
        filtered.append(t)

    return filtered

def filter2(vertices, triangles):

    filtered = []
    for t in triangles:
        idx = t[0]
        if vertices[idx][1] > 0:
            continue
        idx = t[1]
        if vertices[idx][1] > 0:
            continue
        idx = t[2]
        if vertices[idx][1] > 0:
            continue
        filtered.append(t)

    return filtered

def filter3(vertices, triangles):

    filtered = []
    for t in triangles:
        idx = t[0]
        if vertices[idx][1] < 0:
            continue
        idx = t[1]
        if vertices[idx][1] < 0:
            continue
        idx = t[2]
        if vertices[idx][1] < 0:
            continue
        filtered.append(t)

    return filtered

def filter4(vertices, triangles):

    filtered = []
    for t in triangles:
        idx = t[0]
        if vertices[idx][2] > 0:
            continue
        idx = t[1]
        if vertices[idx][2] > 0:
            continue
        idx = t[2]
        if vertices[idx][2] > 0:
            continue
        filtered.append(t)

    return filtered

def filter5(vertices, triangles):

    filtered = []
    for t in triangles:
        idx = t[0]
        if vertices[idx][2] < 0:
            continue
        idx = t[1]
        if vertices[idx][2] < 0:
            continue
        idx = t[2]
        if vertices[idx][2] < 0:
            continue
        filtered.append(t)

    return filtered

def filter6(vertices, triangles):

    filtered = []
    for t in triangles:
       
        if vertices[t[0]][0] > 0 and vertices[t[1]][0] > 0 and vertices[t[2]][0] > 0:
            continue

        filtered.append(t)

    return filtered

def filter7(vertices, triangles):

    filtered = []
    for t in triangles:
       
        if vertices[t[0]][0] < 0 and vertices[t[1]][0] < 0 and vertices[t[2]][0] < 0:
            continue

        filtered.append(t)

    return filtered

def filter8(vertices, triangles):

    filtered = []
    for t in triangles:
       
        if vertices[t[0]][1] > 0 and vertices[t[1]][1] > 0 and vertices[t[2]][1] > 0:
            continue

        filtered.append(t)

    return filtered

def filter9(vertices, triangles):

    filtered = []
    for t in triangles:
       
        if vertices[t[0]][1] < 0 and vertices[t[1]][1] < 0 and vertices[t[2]][1] < 0:
            continue

        filtered.append(t)

    return filtered

def filter10(vertices, triangles):

    filtered = []
    for t in triangles:
       
        if vertices[t[0]][2] > 0 and vertices[t[1]][2] > 0 and vertices[t[2]][2] > 0:
            continue

        filtered.append(t)

    return filtered

def filter11(vertices, triangles):

    filtered = []
    for t in triangles:
       
        if vertices[t[0]][2] < 0 and vertices[t[1]][2] < 0 and vertices[t[2]][2] < 0:
            continue

        filtered.append(t)

    return filtered


def filter_mesh(mesh, mode):

    filtered_mesh = None
    filtered = None

    if mesh is None:
        print('mesh is None')

    elif mode < 0 or mode > 11:
        print('invalid mode(%d)' % mode)

    else:
        vertices  = np.asarray(mesh.vertices)
        triangles = np.asarray(mesh.triangles)
        colors    = np.asarray(mesh.vertex_colors)

        if mode == 0:
            filtered = filter0(vertices, triangles)
        elif mode == 1:
            filtered = filter1(vertices, triangles)
        elif mode == 2:
            filtered = filter2(vertices, triangles)
        elif mode == 3:
            filtered = filter3(vertices, triangles)
        elif mode == 4:
            filtered = filter4(vertices, triangles)
        elif mode == 5:
            filtered = filter5(vertices, triangles)
        elif mode == 6:
            filtered = filter6(vertices, triangles)
        elif mode == 7:
            filtered = filter7(vertices, triangles)
        elif mode == 8:
            filtered = filter8(vertices, triangles)
        elif mode == 9:
            filtered = filter9(vertices, triangles)
        elif mode == 10:
            filtered = filter10(vertices, triangles)
        elif mode == 11:
            filtered = filter11(vertices, triangles)

        filtered_mesh = o3d.geometry.TriangleMesh()
        filtered_mesh.vertices = o3d.utility.Vector3dVector(vertices)
        filtered_mesh.triangles = o3d.utility.Vector3iVector(filtered)
        filtered_mesh.vertex_colors = o3d.utility.Vector3dVector(colors)        
        filtered_mesh.remove_unreferenced_vertices()
        #filtered_mesh.compute_vertex_normals()

    return filtered_mesh
