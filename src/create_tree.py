import numpy as np
import matplotlib.pyplot as plt
from skimage import measure
import open3d as o3d
import os

SCALE_LENGTH = 0.85
SCALE_RADIUS = 0.65
DEPTH = 4
RES = 50

fTerminate = False
fSave = False

# ==========================================
# 1. 基本的な数学・SDF関数の定義
# ==========================================

def smin(a, b, k=0.1):
    """2つのSDFを滑らかに結合する関数 (Smooth Minimum)"""
    h = np.maximum(k - np.abs(a - b), 0.0) / k
    return np.minimum(a, b) - h * h * h * k * (1.0 / 6.0)

def sd_capsule(p, a, b, r):
    """カプセル（太さのある枝）のSDF
    p: (N, 3) 空間の座標の配列
    a, b: 枝の始点と終点 (3,)
    r: 枝の半径
    """
    pa = p - a
    ba = b - a
    b_len_sq = np.dot(ba, ba)
    
    # 各点から線分への射影の割合 (0.0 〜 1.0 にクランプ)
    h = np.clip(np.dot(pa, ba) / b_len_sq, 0.0, 1.0)
    
    # 線分からの最短距離を計算
    dist = np.linalg.norm(pa - ba[:, np.newaxis].T * h[:, np.newaxis], axis=1)
    return dist - r

def pseudo_noise_3d(p):
    """グリッド上での計算用に適した軽量な擬似3Dサインノイズ
    (重いパーリンノイズの代わりに、有機的な歪みを作るための代用)
    """
    return (np.sin(p[:, 0] * 5.0) * np.cos(p[:, 1] * 5.0) * np.sin(p[:, z_idx := 2] * 5.0)) * 0.05

# ==========================================
# 2. 乱数（シード）によるツリー構造（骨格）の生成
# ==========================================

# 乱数シードの固定（毎回同じ木にする場合。変えれば違う木になります）
# np.random.seed(42)

branches = [] # (start, end, radius) のリスト

def generate_tree_structure(start, direction, length, radius, depth):
    if depth == 0 or length < 0.1:
        return
    
    # 終点の計算
    end = start + direction * length
    branches.append((start, end, radius))
    
    # 次の分岐（2本に分かれる）
    num_splits = 2
    for _ in range(num_splits):
        # 元の方向ベクトルにランダムな揺らぎを加える
        random_offset = np.random.uniform(-0.5, 0.5, size=3)
        new_dir = direction + random_offset
        new_dir /= np.linalg.norm(new_dir) # 正規化
        
        # 枝を少し短く、細くして再帰呼び出し
        generate_tree_structure(end, new_dir, length * SCALE_LENGTH, radius * SCALE_RADIUS, depth - 1)

# 木の骨格を生成開始 (始点, 上方向ベクトル, 初期長, 初期太さ, 再帰深さ)
generate_tree_structure(np.array([0.0, 0.0, -0.8]), np.array([0.0, 0.0, 1.0]), 0.6, 0.12, DEPTH)

# ==========================================
# 3. 空間全体のSDF評価（シーンの構築）
# ==========================================

def scene_sdf(p):
    # ① 空間自体にノイズを加えて「うねり」を作る（ドメインワーピング）
    p_warped = p.copy()
    p_warped += np.stack([pseudo_noise_3d(p), pseudo_noise_3d(p + 1.0), pseudo_noise_3d(p + 2.0)], axis=1)
    
    # 初期値は十分に大きな距離
    overall_dist = np.full(p.shape[0], 1e5)
    
    # すべての枝のSDFをスムーズに結合
    for start, end, radius in branches:
        d_branch = sd_capsule(p_warped, start, end, radius)
        overall_dist = smin(overall_dist, d_branch, k=0.08)
        
    return overall_dist

def key_callback_set_save_flag(vis, action, mods):

    global fTerminate, fSave
    
    fSave = True
    fTerminate = True
    vis.destroy_window()

    return False

# ==========================================
# 4. メッシュ化とレンダリング
# ==========================================

# 3D空間のグリッド（解像度）の設定
# ※高くすると高精細になりますが、計算時間がかかります（まずは40〜60程度がおすすめ）
grid_res = RES
x = np.linspace(-1.2, 1.2, grid_res)
y = np.linspace(-1.2, 1.2, grid_res)
z = np.linspace(-1.0, 1.2, grid_res)
X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

# グリッドの点を平坦化してSDFを一括評価
points = np.stack([X.ravel(), Y.ravel(), Z.ravel()], axis=1)
sdf_values = scene_sdf(points)
volume = sdf_values.reshape(grid_res, grid_res, grid_res)

# マーチングキューブ法でSDF=0（表面）のポリゴンを抽出
# spacingを指定して実際の空間スケールに合わせる
spacing = (x[1]-x[0], y[1]-y[0], z[1]-z[0])
verts, faces, normals, values = measure.marching_cubes(volume, level=0.0, spacing=spacing)

# 描画位置のオフセット（グリッドの開始地点を足す）
verts += np.array([x[0], y[0], z[0]])

mesh = o3d.geometry.TriangleMesh()
mesh.vertices = o3d.utility.Vector3dVector(np.asarray(verts))
mesh.triangles = o3d.utility.Vector3iVector(np.asarray(faces))
mesh.compute_vertex_normals()

mesh2 = o3d.geometry.TriangleMesh()
mesh2.vertices = o3d.utility.Vector3dVector(np.asarray(verts))
mesh2.triangles = o3d.utility.Vector3iVector(np.asarray(faces[:,[0,2,1]]))
mesh2.compute_vertex_normals()

vis = o3d.visualization.VisualizerWithKeyCallback()
vis.create_window()
vis.add_geometry(mesh+mesh2)
vis.register_key_action_callback(ord("S"), key_callback_set_save_flag)

print('Hit s-key to save and terminate')
print('Hit ESC-key to quit')

vis.run()

vis.destroy_window()

if fSave:
    no = 1
    dst_path = 'tree.ply'
    while os.path.exists(dst_path):
        no += 1
        dst_path = 'tree_%d.ply' % no

    o3d.io.write_triangle_mesh(dst_path, mesh+mesh2)
    print('save %s' % dst_path)
