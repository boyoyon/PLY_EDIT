import numpy as np
import open3d as o3d

def lid(points,color_front, color_back, height = 0.0):

    nr_points = len(points)

    _points = np.array(points)

    centroid = np.mean(_points, axis=0)
    centered = _points - centroid

    mean_radius = np.mean(np.linalg.norm(centered, axis=1))
    cov = np.cov(centered.T)
    _, eig_vecs = np.linalg.eigh(cov)
    mean_normal = eig_vecs[:,0]

    center = centroid + mean_normal * mean_radius * height

    _points = np.vstack([_points, center])

    triangles = []

    for i in range(1, nr_points):
        triangles.append((nr_points, i-1, i))
    triangles.append((nr_points, nr_points - 1, 0))

    triangles = np.array(triangles)

    _color_front = np.array(color_front) / 255.0
    fgc = np.tile(_color_front, (nr_points+1, 1))

    _color_back = np.array(color_back) / 255.0
    bgc = np.tile(_color_back, (nr_points+1, 1))

    mesh_front = o3d.geometry.TriangleMesh()
    mesh_front.vertices = o3d.utility.Vector3dVector(_points)
    mesh_front.triangles = o3d.utility.Vector3iVector(triangles)
    mesh_front.vertex_colors = o3d.utility.Vector3dVector(fgc)

    mesh_back = o3d.geometry.TriangleMesh()
    mesh_back.vertices = o3d.utility.Vector3dVector(_points)
    mesh_back.triangles = o3d.utility.Vector3iVector(triangles[:,[0,2,1]])
    mesh_back.vertex_colors = o3d.utility.Vector3dVector(bgc)

    return mesh_front + mesh_back
