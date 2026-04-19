import open3d as o3d
import sys

argv = sys.argv
argc = len(argv)

print('%s displays translucent mesh' % argv[0])
print('[usage] python %s <mesh>' % argv[0])

if argc < 2:
    quit()

# PLYの読み込み
mesh = o3d.io.read_triangle_mesh(argv[1])
mesh.compute_vertex_normals()

# 描画オプションの設定
# 注意: バージョンによってAPIが異なる場合があります
mat = o3d.visualization.rendering.MaterialRecord()
mat.shader = "defaultLitTransparency"
mat.base_color = [0.1, 0.6, 0.9, 0.5] # 最後の値がAlpha(透過度)

o3d.visualization.draw([{"name": "mesh", "geometry": mesh, "material": mat}])
