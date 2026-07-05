import numpy as np
import open3d as o3d
from scipy.spatial.transform import Rotation as R

# 平行移動フレーム（Parallel Transport Frame / Bishop Frame）でねじれ防止

def p_polyline(points, section):

    trajectory = np.array(points)

    cross_section = None

    if np.array(section).ndim == 3:
        cross_section = np.array(section[-1])
    else:
        cross_section = np.array(section) 

    # z軸向きになるように回転
    R0 = o3d.geometry.get_rotation_matrix_from_xyz((0, np.pi/2, np.pi/2)) 
    cross_section = cross_section @ R0.T   

    """
    Parallel Transport Frame (Bishop Frame) を使用したスィープ面の生成
    
    cross_section: (N, 3) の numpy array (Z=0 平面上の切り口)
    trajectory: (M, 3) の numpy array (軌道)
    戻り値: (M, N, 3) の sweep面点群
    """
    M = len(trajectory)
    N = len(cross_section)
    
    # 1. 軌道の接線ベクトル（方向）の計算
    tangents = np.zeros_like(trajectory)
    tangents[1:-1] = trajectory[2:] - trajectory[:-2]
    tangents[0] = trajectory[1] - trajectory[0]
    tangents[-1] = trajectory[-1] - trajectory[-2]
    
    norms = np.linalg.norm(tangents, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    tangents /= norms

    # 2. 初期フレーム（クォータニオン）の決定
    initial_vector = np.array([0.0, 0.0, 1.0]) # 切り口の初期法線
    sweep_vertices = np.zeros((M, N, 3))
    
    # 最初の点における回転
    if np.allclose(tangents[0], initial_vector):
        current_rotation = R.identity()
    elif np.allclose(tangents[0], -initial_vector):
        current_rotation = R.from_euler('x', 180, degrees=True)
    else:
        current_rotation, _ = R.align_vectors([tangents[0]], [initial_vector])
    
    # 最初の点を配置
    sweep_vertices[0] = current_rotation.apply(cross_section) + trajectory[0]

    # 3. 2点目以降は、前後の接線間の「最小回転」を累積させていく
    for i in range(1, M):
        t_prev = tangents[i-1]
        t_curr = tangents[i]
        
        # 2つのベクトル間の外積（回転軸）と内積（角度の元）から最小回転を計算
        dot = np.dot(t_prev, t_curr)
        dot = np.clip(dot, -1.0, 1.0) # 数値誤差対策
        
        if np.allclose(dot, 1.0):
            # 方向が変わっていない場合は回転なし
            delta_rotation = R.identity()
        elif np.allclose(dot, -1.0):
            # 真逆を向く場合は、直前のフレームの主軸（例: X軸）まわりに180度回転
            # （激しい折り返し軌道でない限り通常は発生しません）
            axis = current_rotation.apply([1.0, 0.0, 0.0])
            delta_rotation = R.from_rotvec(axis * np.pi)
        else:
            # 最小回転の軸と角度を計算
            axis = np.cross(t_prev, t_curr)
            axis /= np.linalg.norm(axis)
            angle = np.arccos(dot)
            delta_rotation = R.from_rotvec(axis * angle)
        
        # クォータニオンの合成（前の回転に今回の微小回転を掛け合わせる）
        # ※ scipy の Rotation は「右から結合」で累積されます
        current_rotation = delta_rotation * current_rotation
        
        # 回転と移動を適用
        sweep_vertices[i] = current_rotation.apply(cross_section) + trajectory[i]
        
    sweep_vertices = sweep_vertices[:,::-1,:] # 裏表が従来と同じになるようにする

    return sweep_vertices.tolist()

