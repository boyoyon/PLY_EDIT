import open3d as o3d
import manifold3d
from manifold3d import Manifold
import numpy as np
import copy, os, sys

def manifold_to_mesh(mani):
    # 演算後のデータをOpen3D形式に戻す
    m = mani.to_mesh()

    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(m.vert_properties)

    triangles = copy.deepcopy(m.tri_verts)
    #mesh.triangles = o3d.utility.Vector3iVector(m.tri_verts)
    mesh.triangles = o3d.utility.Vector3iVector(triangles)
    return mesh

def mesh_to_manifold(o3d_mesh):
    # 1. 頂点と面を抽出し、型を指定
    verts = np.asarray(o3d_mesh.vertices, dtype=np.float32)
    tri_indices = np.asarray(o3d_mesh.triangles, dtype=np.int32)
    
    # 2. manifold3d.Mesh オブジェクトを作成
    # ※辞書ではなく、キーワード引数でプロパティを渡します
    mani_mesh = manifold3d.Mesh(
        vert_properties=verts,
        tri_verts=tri_indices
    )
    
    # 3. MeshオブジェクトをManifoldコンストラクタに渡す
    return manifold3d.Manifold(mani_mesh)

argv = sys.argv
argc = len(argv)

print('%s executes boolean operation (mesh_A - mesh_B)' % argv[0])
print('[usage] python %s <mesh_A> <mesh_B>' % argv[0])

if argc < 3:
    quit()

mesh_a = o3d.io.read_triangle_mesh(argv[1])           
mesh_b = o3d.io.read_triangle_mesh(argv[2])           

"""
base = os.path.basename(argv[1])
filename = os.path.splitext(base)[0]
dst_path = '%s_text.ply' % filename

o3d.io.write_triangle_mesh(dst_path, mesh_a, write_ascii=True)
print('save %s' % dst_path)
"""

# --- ブーリアン演算 ---
mani_a = mesh_to_manifold(mesh_a)
mani_b = mesh_to_manifold(mesh_b)

# 差分 (AからBを引く)
result_mani = mani_a - mani_b

# メッシュに戻して表示
result_mesh = manifold_to_mesh(result_mani)
result_mesh.compute_vertex_normals()

base = os.path.basename(argv[1])
filenameA = os.path.splitext(base)[0]
base = os.path.basename(argv[2])
filenameB = os.path.splitext(base)[0]
dst_path = '%s_minus_%s.ply' % (filenameA, filenameB)

o3d.io.write_triangle_mesh(dst_path, result_mesh)
print('save %s' % dst_path)

o3d.visualization.draw_geometries([result_mesh])
