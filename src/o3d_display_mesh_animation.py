import open3d as o3d
import numpy as np
import sys

mesh = None

delta = 0.5

def animation_callback(vis):
    # ここにアニメーションの更新処理を記述する
    # 例: 点群を少し回転させる
    R = mesh.get_rotation_matrix_from_xyz((0, np.radians(delta), 0))
    mesh.rotate(R, center=(0, 0, 0))
    # ジオメトリの更新をVisualizerに通知
    vis.update_geometry(mesh)
    # 描画の更新
    vis.update_renderer()
    
    return False

def main():

    global mesh

    argv = sys.argv
    argc = len(argv)

    print('%s animate ply' % argv[0])
    print('[usage] python %s <ply file> [<-normal>]' % argv[0])

    if argc < 2:
        quit() 

    # サンプルの点群データを作成
    mesh =  o3d.io.read_triangle_mesh(argv[1])

    fNormal = False
    if argc > 2 and argv[2] == '-normal':
        fNormal = True
    
    if fNormal:
       mesh.compute_vertex_normals()
 
    # アニメーションコールバック付きで描画
    # 'animation_callback'はフレームごとに呼び出され、ジオメトリを更新する
    o3d.visualization.draw_geometries_with_animation_callback([mesh], animation_callback)

if __name__ == '__main__':
    main()
