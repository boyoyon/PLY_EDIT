import open3d as o3d
import numpy as np

def get_boundary_points(mesh):

    # 全てのエッジを抽出 (各面の3辺)
    triangles = np.asarray(mesh.triangles)
    edges = np.concatenate([
        triangles[:, [0, 1]],
        triangles[:, [1, 2]],
        triangles[:, [2, 0]]
    ], axis=0)
    
    # エッジをソートして一意にする (方向を無視してカウントするため)
    edges = np.sort(edges, axis=1)
    
    # 各エッジの出現回数をカウント
    unique_edges, counts = np.unique(edges, axis=0, return_counts=True)
    
    # 出現回数が1回のエッジが「境界エッジ」
    boundary_edges = unique_edges[counts == 1]
    
    # 境界エッジに含まれる頂点インデックスを一意に取得
    boundary_vertex_indices = np.unique(boundary_edges)
    
    # 実際の座標を取得したい場合
    boundary_points = np.asarray(mesh.vertices)[boundary_vertex_indices]

    return boundary_points
