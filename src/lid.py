import numpy as np
import open3d as o3d

def lid(points,color_front, color_back, height = 0.0, shape = 'line'):

    nr_points = len(points)

    height *= -1

    _points = np.array(points)
    triangles = []

    centroid = np.mean(_points, axis=0)
    centered = _points - centroid

    mean_radius = np.mean(np.linalg.norm(centered, axis=1))
    cov = np.cov(centered.T)
    _, eig_vecs = np.linalg.eigh(cov)
    mean_normal = eig_vecs[:,0]

    center = centroid + mean_normal * mean_radius * height

    if shape == 'sphere':

        _points = np.empty((nr_points * nr_points + 1, 3), np.float32)

        for i in range(nr_points):
         
            alpha = i / (nr_points - 1)
            beta = (nr_points - 1 - i) / (nr_points - 1)
            gamma = np.sqrt(1 - beta**2)
    
            idx = nr_points * i

            for j in range(nr_points):

                _p = np.array(points[j]) * beta + centroid * alpha + gamma * mean_radius * height * mean_normal 
                _points[idx] = _p
                idx += 1

        _points[idx] = center

        for i in range(nr_points - 1):
            for j in range(nr_points):

                idx0 = i * nr_points + j
                idx1 = (i + 1) * nr_points + j
                idx2 = i * nr_points + ((j + 1) % nr_points)
                idx3 = (i + 1) * nr_points + ((j + 1) % nr_points)

                triangles.append((idx0,idx3, idx1))
                triangles.append((idx3, idx0, idx2))

        for j in range(nr_points):

            idx0 = _points.shape[0] - 1
            idx1 = (nr_points - 1) * nr_points + j
            idx2 = (nr_points - 1) * nr_points + ((j+1) % nr_points)

            triangles.append((idx0, idx1, idx2))

    else:

        _points = np.array(points)
        _points = np.vstack([_points, center])
    
        for i in range(1, nr_points):
            triangles.append((nr_points, i-1, i))
        triangles.append((nr_points, nr_points - 1, 0))
    
        triangles = np.array(triangles)

    triangles = np.array(triangles)

    _color_front = np.array(color_front) / 255.0
    fgc = np.tile(_color_front, (_points.shape[0], 1))

    _color_back = np.array(color_back) / 255.0
    bgc = np.tile(_color_back, (_points.shape[0], 1))

    mesh_front = o3d.geometry.TriangleMesh()
    mesh_front.vertices = o3d.utility.Vector3dVector(_points)
    mesh_front.triangles = o3d.utility.Vector3iVector(triangles)
    mesh_front.vertex_colors = o3d.utility.Vector3dVector(fgc)

    mesh_back = o3d.geometry.TriangleMesh()
    mesh_back.vertices = o3d.utility.Vector3dVector(_points)
    mesh_back.triangles = o3d.utility.Vector3iVector(triangles[:,[0,2,1]])
    mesh_back.vertex_colors = o3d.utility.Vector3dVector(bgc)

    return mesh_front + mesh_back
