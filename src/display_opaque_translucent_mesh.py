import open3d as o3d
import sys

argv = sys.argv
argc = len(argv)

print('%s displays opaque mesh and translucent mesh' % argv[0])
print('[usage] python %s <opaque mesh> <translucent mesh>' % argv[0])

if argc < 3:
    quit()

# 1. ジオメトリの読み込み
opaque_mesh = o3d.io.read_triangle_mesh(argv[1]) # 不透明
translucent_mesh = o3d.io.read_triangle_mesh(argv[2]) # 半透明

# 2. 不透明オブジェクト用マテリアル
mat_opaque = o3d.visualization.rendering.MaterialRecord()
mat_opaque.shader = "defaultLit"

# 3. 半透明オブジェクト用マテリアル
mat_translucent = o3d.visualization.rendering.MaterialRecord()
mat_translucent.shader = "defaultLitTransparency"
mat_translucent.base_color = [0.0, 0.0, 1.0, 0.5] 

# 4. 表示
o3d.visualization.draw([
    {"name": "opaque_obj", "geometry": opaque_mesh, "material": mat_opaque},
    {"name": "translucent_obj", "geometry": translucent_mesh, "material": mat_translucent}
])
